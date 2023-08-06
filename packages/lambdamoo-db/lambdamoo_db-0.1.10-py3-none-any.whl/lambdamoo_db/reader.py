from . import templates
from .enums import DBVersions, MooTypes, PropertyFlags
from .database import (
    VM,
    Anon,
    ObjNum,
    Waif,
    Activation,
    MooDatabase,
    MooObject,
    Property,
    QueuedTask,
    SuspendedTask,
    Verb,
    WaifReference,
)
from typing import Any, NoReturn, Pattern, Union
import parse
import re
from io import TextIOWrapper
from logging import getLogger
logger = getLogger(__name__)


def load(filename: str) -> MooDatabase:
    with open(filename, "r", encoding="latin-1") as f:
        r = Reader(f, filename)
        return r.parse()


def compile(template: str) -> Pattern[str]:
    compiled = parse.compile(template)
    if compiled._match_re is None:
        raise Exception(f"Failed to compile template: {template}")
    return compiled._match_re


versionRe = compile(templates.version)
varCountRe = compile(templates.var_count)
clockCountRe = compile(templates.clock_count)
taskCountRe = compile(templates.task_count)
taskHeaderRe = compile(templates.task_header)
activationHeaderRe = compile(templates.activation_header)
pendingValueRe = compile(templates.pending_values_count)
suspendedTaskCountRe = compile(templates.suspended_task_count)
suspendedTaskHeaderRe = compile(templates.suspended_task_header)
interruptedTaskCountRe = compile(templates.interrupted_task_count)
interruptedTaskHeaderRe = re.compile(r"(?P<id>\d+) (?P<status>[\w\W]+)")
vmHeaderRe = compile(templates.vm_header)
connectionCountRe = re.compile(r"(?P<count>\d+) active connections(?P<listener_tag>| with listeners)")
langverRe = compile(templates.langver)
stackheaderRe = compile(templates.stack_header)
pcRe = compile(templates.pc)
waifHeaderRe = compile(templates.waif_header)


class Reader:
    def __init__(self, fio: TextIOWrapper, filename: str = "") -> None:
        self.filename = filename
        self.file = fio
        self.line = 0

    def parse_error(self, message: str) -> NoReturn:
        raise Exception(f"Parse Error: {self.filename}:{self.line} : {message}")

    def parse(self) -> "MooDatabase":
        db = MooDatabase()
        db.waifs = {}
        db.versionstring = self.readString()
        version = versionRe.match(db.versionstring)
        if not version:
            self.parse_error("Invalid version string")
        db.version = int(version.group("version"))
        match db.version:
            case 4:
                self.parse_v4(db)
            case 17:
                self.parse_v17(db)
            case _:
                self.parse_error(f"Unknown db version {db.version}")
        return db

    def parse_v4(self, db: MooDatabase) -> None:
        logger.debug("Parsing v4 database")
        db.total_objects = self.readInt()
        db.total_verbs = self.readInt()
        self.readString()  # dummy
        self.readPlayers(db)
        self.readObjects(db)
        self.readVerbs(db)
        self.readClocks(db)
        self.readTaskQueue(db)
        self.readSuspendedTasks(db)
        self.readConnections()

    def parse_v17(self, db: MooDatabase) -> None:
        logger.debug("Parsing v17 database")
        self.readPlayers(db)
        self.readPending(db)
        self.readClocks(db)
        self.readTaskQueue(db)
        self.readSuspendedTasks(db)
        self.readInterruptedTasks(db)
        self.readConnections()
        db.total_objects = self.readInt()
        self.readObjects(db)
        if db.version >= DBVersions.DBV_Anon:
            self.readAnonObjects(db)
        db.total_verbs = self.readInt()
        self.readVerbs(db)

    def readValue(self, db: MooDatabase, *, known_type: int | None = None) -> Any:
        if known_type is not None:
            val_type = known_type
        else:
            val_type = self.readInt()
        match val_type:
            case MooTypes.STR:
                return self.readString()
            case MooTypes.OBJ:
                return self.readObjnum()
            case MooTypes.ANON:
                return self.readAnon(db)
            case MooTypes.INT:
                return self.readInt()
            case MooTypes.FLOAT:
                return self.readFloat()
            case MooTypes.ERR:
                return self.readErr()
            case MooTypes.LIST:
                return self.readList(db)
            case MooTypes.CLEAR:
                pass
            case MooTypes.NONE:
                pass
            case MooTypes.MAP:
                return self.readMap(db)
            case MooTypes.BOOL:
                return self.readBool()
            case MooTypes._CATCH:
                return self.readInt()
            case MooTypes._FINALLY:
                return self.readInt()
            case MooTypes.WAIF:
                return self.readWaif(db)
            case _:
                self.parse_error(f"unknown type {val_type}")

    def readString(self) -> str:
        """Read a string from the database file"""
        self.line += 1
        return self.file.readline().rstrip("\r\n")

    def readInt(self) -> int:
        """Read an integer from the database file"""
        return int(self.readString())

    def readErr(self) -> int:
        return self.readInt()

    def readFloat(self) -> float:
        return float(self.readString())

    def readObjnum(self) -> ObjNum:
        return ObjNum(self.readString())

    def readBool(self) -> bool:
        return bool(self.readInt())

    def readList(self, db: MooDatabase) -> list[Any]:
        length = self.readInt()
        result = []
        for _ in range(length):
            result.append(self.readValue(db))
        return result

    def readMap(self, db: MooDatabase) -> dict:
        # self.parse_error(f'MAP @ Line {self.line}')
        items = self.readInt()
        map = {}
        for _ in range(items):
            key = self.readValue(db)
            val = self.readValue(db)
            map[key] = val
        return map

    def readWaif(self, db: MooDatabase):
        #  waif.cc:950 read_waif()
        header = waifHeaderRe.match(self.readString())
        if not header:
            self.parse_error(f"Invalid waif header")
        index = int(header.group("index"))
        if header.group("flag") == "r":
            # Reference
            _terminator = self.readString()
            return WaifReference(index)

        _class = self.readObjnum()
        owner = self.readObjnum()
        props = []
        new = Waif(_class, owner, props)
        propdefs_length = self.readInt()

        db.waifs[index] = new
        while (cur := self.readInt()) < 3 * 32 and cur > -1:
            props.append(self.readValue(db))
        _terminator = self.readString()
        return WaifReference(index)

    def readObject_v4(self, db: MooDatabase) -> Union[MooObject, None]:
        objNumber = self.readString()
        if not objNumber.startswith("#"):
            self.parse_error("object number does not have #")

        if "recycled" in objNumber:
            logger.debug(f"Skipping recycled object {objNumber}")
            return None

        oid = int(objNumber[1:])
        name = self.readString()
        self.readString()  # blankline
        flags = self.readInt()
        owner = self.readObjnum()
        location = self.readObjnum()
        firstContent = self.readInt()
        neighbor = self.readInt()
        parent = self.readObjnum()
        firstChild = self.readInt()
        sibling = self.readInt()
        obj = MooObject(
            id=oid,
            name=name,
            flags=flags,
            owner=owner,
            location=location,
            parents=[parent],
        )
        numVerbs = self.readInt()
        for _ in range(numVerbs):
            self.readVerbMetadata(obj)

        self.readProperties(db, obj)
        logger.debug(f"Read object {oid} {obj.name}")
        return obj

    def readObject_ng(self, db: MooDatabase) -> Union[MooObject, None]:
        objNumber = self.readString()
        if not objNumber.startswith("#"):
            self.parse_error("object number does not have #")

        if "recycled" in objNumber:
            logger.debug(f"Skipping recycled object {objNumber}")
            return None

        oid = int(objNumber[1:])
        name = self.readString()
        flags = self.readInt()
        owner = self.readObjnum()
        location = self.readValue(db)
        if db.version >= DBVersions.DBV_Last_Move:
            last_move = self.readValue(db)

        contents = self.readValue(db)
        parents = self.readValue(db)
        if not isinstance(parents, list):
            parents = [parents]
        children = self.readValue(db)
        obj = MooObject(oid, name, flags, owner, location, parents)
        numVerbs = self.readInt()
        for _ in range(numVerbs):
            self.readVerbMetadata(obj)

        self.readProperties(db, obj)
        logger.debug(f"Read object {oid} {obj.name}")
        return obj

    def readAnon(self, db: MooDatabase) -> None:
        oid = self.readInt()
        if oid == -1:
            self.parse_error("Not sure what to do with a -1 anon yet")
        else:
            return Anon(oid)

    def readConnections(self) -> None:
        header = self.readString()
        headerMatch = connectionCountRe.match(header)
        if not headerMatch:
            self.parse_error("Bad active connections header line")

        count = int(headerMatch.group("count"))
        for _ in range(count):
            # Read and discard `count` lines; this data is useless to us.
            self.readString()

    def readVerbs(self, db: MooDatabase) -> None:
        logger.debug(f"Reading {db.total_verbs} verbs")
        for _ in range(db.total_verbs):
            self.readVerb(db)
        logger.debug(f"Finished reading {db.total_verbs} verbs")

    def readVerb(self, db: MooDatabase) -> None:
        verbLocation = self.readString()
        if ":" not in verbLocation:
            self.parse_error("verb does not have seperator")

        sep = verbLocation.index(":")
        objNumber = int(verbLocation[1:sep])
        verbNumber = int(verbLocation[sep + 1:])
        code = self.readCode()
        obj = db.objects.get(objNumber)
        if not obj:
            self.parse_error(f"object {objNumber} not found")

        verb = obj.verbs[verbNumber]
        if not verb:
            self.parse_error(f"verb ${verbNumber} not found on object ${objNumber}")

        verb.object = objNumber
        verb.code = code

    def readCode(self) -> list[str]:
        code = []
        lastLine = self.readString()
        while lastLine != ".":
            code.append(lastLine)
            lastLine = self.readString()
        return code

    def readPlayers(self, db: MooDatabase) -> None:
        db.total_players = self.readInt()
        logger.debug(f"Reading {db.total_players} players")
        db.players = []
        for _ in range(db.total_players):
            db.players.append(self.readObjnum())
        assert db.total_players == len(db.players)
        logger.debug(f"Finished reading {db.total_players} players")

    def readAnonObjects(self, db: MooDatabase) -> None:
        while True:
            num_anon = self.readInt()
            if num_anon == 0:
                break
            if num_anon > 0:
                for i in range(num_anon):
                    obj = self.readObject_ng(db)
                    obj.anon = True
                    db.objects[obj.id] = obj

    def readObjects(self, db: MooDatabase) -> None:
        db.objects = {}
        for _ in range(db.total_objects):
            if db.version == 4:
                obj = self.readObject_v4(db)
            else:
                obj = self.readObject_ng(db)
            if not obj:
                continue
            db.objects[obj.id] = obj
        for o in db.objects.values():
            self.process_propnames(db, o)

    def process_propnames(self, db: MooDatabase, obj: MooObject) -> None:
        names = []
        parent = obj
        while parent is not None:
            names.extend(p.propertyName for p in parent.properties if p.propertyName is not None)
            if len(parent.parents) > 1:
                # todo: Identify order of multi-inheritence
                break
            parent = db.objects.get(parent.parent)
        i = 1
        for p in obj.properties:
            try:
                n = names.pop(0)
            except IndexError:
                n = i
            if not p.propertyName:
                p.propertyName = n
            elif n != p.propertyName:
                self.parse_error(f"property name mismatch: {n} != {p.propertyName}")
            i += 1

    def readVerbMetadata(self, obj: MooObject) -> None:
        name = self.readString()
        owner = self.readObjnum()
        perms = self.readInt()
        preps = self.readInt()
        verb = Verb(name, owner, perms, preps, -1)
        obj.verbs.append(verb)

    def readProperties(self, db: MooDatabase, obj: MooObject):
        numProperties = self.readInt()
        propertyNames = []
        for _ in range(numProperties):
            propertyNames.append(self.readString())
        numPropdefs = self.readInt()
        for _ in range(numPropdefs):
            propertyName = None
            if propertyNames:
                propertyName = propertyNames.pop(0)
            value = self.readValue(db)
            owner = self.readObjnum()
            perms = PropertyFlags(self.readInt())
            property = Property(propertyName, value, owner, perms)
            obj.properties.append(property)

    def readPending(self, db: MooDatabase) -> None:
        valueLine = self.readString()
        valueMatch = pendingValueRe.match(valueLine)
        if not valueMatch:
            self.parse_error("Bad pending finalizations")

        finalizationCount = int(valueMatch.group("count"))
        for _ in range(finalizationCount):
            self.readValue(db)

    def readClocks(self, db: MooDatabase) -> None:
        clockLine = self.readString()
        clockMatch = clockCountRe.match(clockLine)
        if not clockMatch:
            self.parse_error("Could not find clock definitions")
        db.clocks = []
        numClocks = int(clockMatch.group("count"))
        for _ in range(numClocks):
            self.readClock(db)

    def readClock(self, db: MooDatabase) -> None:
        """Obsolete"""
        db.clocks.append(self.readString())

    def readTaskQueue(self, db: MooDatabase) -> None:
        queuedTasksLine = self.readString()
        queuedTasksMatch = taskCountRe.match(queuedTasksLine)
        if not queuedTasksMatch:
            self.parse_error("Could not find task queue")

        numTasks = int(queuedTasksMatch.group("count"))
        logger.debug(f"Reading {numTasks} queued tasks")
        db.queuedTasks = []
        for _ in range(numTasks):
            self.readQueuedTask(db)
        assert numTasks == len(db.queuedTasks)
        logger.debug(f"Finished reading {numTasks} queued tasks")

    def readQueuedTask(self, db: MooDatabase) -> None:
        headerLine = self.readString()
        headerMatch = taskHeaderRe.match(headerLine)
        if not headerMatch:
            self.parse_error("Could not find task header")
        unused = int(headerMatch[1])
        firstLineno = int(headerMatch[2])
        st = int(headerMatch[3])
        id = int(headerMatch[4])
        task = QueuedTask(firstLineno, id, st)
        activation = self.read_activation_as_pi(db)
        task.activation = activation
        task.rtEnv = self.readRTEnv(db)
        task.code = self.readCode()
        task.unused = unused
        db.queuedTasks.append(task)

    def read_activation_as_pi(self, db: MooDatabase) -> Activation:
        _ = self.readValue(db)
        if db.version >= DBVersions.DBV_This:
            _this = self.readValue(db)
        if db.version >= DBVersions.DBV_Anon:
            _vloc = self.readValue(db)
        if db.version >= DBVersions.DBV_Threaded:
            threaded = self.readInt()
        else:
            threaded = 0

        headerLine = self.readString()
        headerMatch = activationHeaderRe.match(headerLine)
        if not headerMatch:  # or headerMatch.length !== 6) {
            self.parse_error("Could not find activation header")

        activation = Activation()
        activation.this = int(headerMatch[1])
        activation.unused1 = int(headerMatch[2])
        activation.threaded = threaded
        activation.unused2 = int(headerMatch[3])
        activation.player = int(headerMatch[4])
        activation.unused3 = int(headerMatch[5])
        activation.programmer = int(headerMatch[6])
        activation.vloc = int(headerMatch[7])
        activation.unused4 = int(headerMatch[8])
        activation.debug = bool(headerMatch[9])
        self.readString()  # /* Was argstr*/
        self.readString()  # /* Was dobjstr*/
        self.readString()  # /* Was prepstr*/
        self.readString()  # /* Was iobjstr*/
        activation.verb = self.readString()
        activation.verbname = self.readString()
        return activation

    def read_activation(self, db: MooDatabase) -> Activation:
        if db.version < DBVersions.DBV_Float:
            pass
        else:
            langver = self.readString()
            if not (langverMatch := langverRe.match(langver)):
                self.parse_error(f"Bad language version header {langver}")

        code = self.readCode()
        rt = self.readRTEnv(db)
        stackheader = self.readString()
        stackheaderMatch = stackheaderRe.match(stackheader)
        if not stackheaderMatch:
            self.parse_error("READ_ACTIV: bad stack header")
        stack = []
        for _ in range(int(stackheaderMatch.group("slots"))):
            _s = self.readValue(db)
            stack.append(_s)
        activation = self.read_activation_as_pi(db)
        activation.stack = stack
        activation.code = code
        activation.stack = stack
        _temp = self.readValue(db)
        pchead = self.readString()
        if not (pcMatch := pcRe.match(pchead)):
            self.parse_error("READ_ACTIV: bad pc")
        if int(pcMatch.group("bi_func")):
            func_name = self.readString()
        return activation

    def readRTEnv(self, db: MooDatabase) -> dict[str, Any]:
        varCountLine = self.readString()
        varCountMatch = varCountRe.match(varCountLine)
        if not varCountMatch:
            self.parse_error("Could not find variable count for RT Env")

        varCount = int(varCountMatch.group("count"))
        logger.debug(f"Reading RTEnv with {varCount} variables")
        rtEnv = {}
        for _ in range(varCount):
            name = self.readString()
            value = self.readValue(db)
            rtEnv[name] = value
        return rtEnv

    def readSuspendedTasks(self, db: MooDatabase) -> None:
        valueLine = self.readString()
        suspendedMatch = suspendedTaskCountRe.match(valueLine)
        if not suspendedMatch:
            self.parse_error("Bad suspended tasks header")

        db.suspendedTasks = []
        count = int(suspendedMatch.group("count"))
        for _ in range(count):
            self.readSuspendedTask(db)

    def readSuspendedTask(self, db: MooDatabase) -> None:
        headerLine = self.readString()
        taskMatch = suspendedTaskHeaderRe.match(headerLine)
        if not taskMatch:
            self.parse_error(f"Bad suspended task header: {headerLine}")

        id = int(taskMatch.group("id"))
        startTime = int(taskMatch.group("startTime"))
        task = SuspendedTask(0, id, startTime)  # Set line number to 0 for a suspended task since we don't know it (only opcodes, not text)
        if val := taskMatch.group("value"):
            task.value = self.readValue(db, known_type=int(val))
        task.vm = self.readVM(db)
        db.suspendedTasks.append(task)

    def readInterruptedTasks(self, db: MooDatabase):
        valueLine = self.readString()
        interruptedMatch = interruptedTaskCountRe.match(valueLine)
        if not interruptedMatch:
            self.parse_error("Bad suspended tasks header")

        count = int(interruptedMatch.group("count"))
        for _ in range(count):
            self.readInterruptedTask(db)

    def readInterruptedTask(self, db: MooDatabase) -> None:
        header = self.readString()
        headerMatch = interruptedTaskHeaderRe.match(header)
        if not headerMatch:
            self.parse_error("Bad interrupted tasks header")
        task_id = headerMatch.group("id")
        vm = self.readVM(db)
        # Shrug
        return None

    def readVM(self, db: MooDatabase) -> VM:
        if db.version >= DBVersions.DBV_TaskLocal:
            local = self.readValue(db)
        else:
            local = {}
        header = self.readString()
        headerMatch = vmHeaderRe.match(header)
        if not headerMatch:
            self.parse_error(f"Bad VM Header {header}")
        top = int(headerMatch.group("top"))
        stack = []
        for _ in range(top + 1):
            stack.append(self.read_activation(db))
        return VM(local, stack)
