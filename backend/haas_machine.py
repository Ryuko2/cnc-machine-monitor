import random
from datetime import datetime
from typing import Dict, Any, List, Optional

class HaasMachine:
    def __init__(
        self,
        machine_id: str,
        name: str,
        model: str,       # "VF-2", "VF-4", "HMC", "LATHE", "PRESS", "LASER"
        mtype: str,       # "CNC_MILL", "LATHE", "PRESS_BRAKE", "LASER"
        specs: Optional[Dict[str, Any]] = None,
    ):
        if specs is None:
            specs = {}

        self.id = machine_id
        self.name = name
        self.model = model
        self.type = mtype

        # Machine Specifications
        axis_limits = specs.get(
            "axisLimits",
            {"X": (0.0, 762.0), "Y": (0.0, 406.0), "Z": (0.0, 508.0)},
        )
        self.specs = {
            "axisLimits": axis_limits,
            "spindlePower": specs.get("spindlePower", 30),          # HP
            "maxRPM": specs.get("maxRPM", 8100),
            "rapidTraverse": specs.get("rapidTraverse", 1000),      # ipm
            "toolCapacity": specs.get("toolCapacity", 24),
            "maxTonnage": specs.get("maxTonnage", 200),
            "maxLaserPower": specs.get("maxLaserPower", 6000),
        }

        # === CORE STATE ===
        self.power: bool = True
        self.execution: str = "IDLE"     # IDLE, RUNNING, ALARM, STOPPED
        self.cyclePhase: str = "IDLE"    # IDLE, SPINDLE_RAMP, RAPID, CUTTING, RETRACT, DWELL, FINISH
        self.timeInPhase: float = 0.0
        self.cycleTimeTarget: float = 20 + random.random() * 25

        # === CRITICAL ALARMS ===
        self.alarm: Optional[str] = None
        self.alarmCode: Optional[int] = None
        self.alarmHistory: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []

        # === SPINDLE DATA ===
        self.spindleSpeed: float = 0.0
        self.targetSpindleSpeed: float = 0.0
        self.spindleLoad: float = 0.0
        self.spindleTemp: float = 25.0
        self.spindleHours: float = 0.0
        self.spindleOrientation: float = 0.0  # degrees

        # === FEED & MOTION ===
        self.feedRate: float = 0.0
        self.targetFeed: float = 0.0
        self.rapidRate: float = 0.0

        self.axisPositions: Dict[str, float] = {
            "X": (axis_limits["X"][0] + axis_limits["X"][1]) / 2.0,
            "Y": (axis_limits["Y"][0] + axis_limits["Y"][1]) / 2.0,
            "Z": axis_limits["Z"][1],  # Safe Z
        }

        # === SERVO MONITORING ===
        self.servoLoad: Dict[str, float] = {"X": 0.0, "Y": 0.0, "Z": 0.0}
        self.servoFollowingError: Dict[str, float] = {"X": 0.0, "Y": 0.0, "Z": 0.0}
        self.servoTemp: Dict[str, float] = {"X": 25.0, "Y": 25.0, "Z": 25.0}

        # === PRODUCTION METRICS ===
        self.partCount: int = 0
        self.totalCycles: int = 0
        self.machineOnHours: float = 0.0
        self.productionRate: int = 0  # parts/hour

        # === HEALTH MONITORING ===
        self.batteryVoltage: float = 3.6
        self.temperature: float = 72.0
        self.vibration: float = 0.0
        self.currentAmps: float = 7.0
        self.oilPressure: float = 50.0
        self.oilLevel: float = 100.0

        # === TOOL MANAGEMENT (CNC/LATHE only) ===
        self.currentTool: Optional[int] = None
        self.tools: Optional[List[Dict[str, Any]]] = None
        self.toolChangeCount: int = 0
        self.toolWear: float = 0.0
        self.coolant: Optional[Dict[str, float]] = None

        if self.type in ("CNC_MILL", "LATHE"):
            self.currentTool = 1
            self.tools = self._initialize_tools()
            self.toolChangeCount = 0
            self.toolWear = 0.0
            self.coolant = {
                "level": 100.0,
                "pressure": 50.0,
                "temperature": 72.0,
                "flow": 0.0,
            }

        # === PRESS BRAKE SPECIFIC ===
        self.tonnage: float = 0.0
        self.maxTonnage: float = self.specs.get("maxTonnage", 200)
        self.ramPosition: float = 0.0
        self.backGauge: float = 0.0
        self.bendAngle: float = 0.0

        # === LASER SPECIFIC ===
        self.laserPower: float = 0.0
        self.maxLaserPower: float = self.specs.get("maxLaserPower", 6000)
        self.gasPressure: float = 240.0
        self.resonatorTemp: float = 26.0
        self.cutSpeed: float = 0.0

        self.material: Optional[str] = None
        self.programRunning: Optional[str] = None
        self.timestamp: datetime = datetime.utcnow()

    # ========================================
    # TOOL INITIALIZATION
    # ========================================

    def _initialize_tools(self) -> List[Dict[str, Any]]:
        tools: List[Dict[str, Any]] = []
        count = self.specs["toolCapacity"] if self.type == "CNC_MILL" else 12
        tool_types = ["DRILL", "END_MILL", "FACE_MILL", "REAMER", "TAP", "BORING_BAR"]
        coatings = ["TiN", "TiCN", "AlTiN", "Uncoated"]

        for i in range(1, count + 1):
            tools.append(
                {
                    "number": i,
                    "type": random.choice(tool_types),
                    "diameter": round(random.random() * 20 + 2, 2),
                    "length": round(random.random() * 100 + 50, 2),
                    "currentLife": 100 - random.random() * 80,
                    "maxLife": 100,
                    "flutes": random.randint(2, 5),
                    "coating": random.choice(coatings),
                    "description": f"Tool {i}",
                    "inUse": False,
                    "totalCuts": 0,
                }
            )
        return tools

    # ========================================
    # MAIN UPDATE LOOP
    # ========================================

    def update(self, dt_sec: float) -> None:
        self.timestamp = datetime.utcnow()

        if not self.power:
            self.execution = "STOPPED"
            self.cyclePhase = "IDLE"
            self.spindleSpeed = 0.0
            self.spindleLoad = 0.0
            self.feedRate = 0.0
            return

        self.machineOnHours += dt_sec / 3600.0
        self.timeInPhase += dt_sec

        # If there is an active alarm
        if self.alarm:
            self.execution = "ALARM"
            self.cyclePhase = "IDLE"
            self.spindleSpeed = max(0.0, self.spindleSpeed - 500.0 * dt_sec)
            self.feedRate = 0.0

            # Auto-recovery (2% chance)
            if random.random() < 0.02:
                self._clear_alarm()
            return

        # Update based on machine type
        if self.type in ("CNC_MILL", "LATHE"):
            self._update_cnc_cycle(dt_sec)
        elif self.type == "PRESS_BRAKE":
            self._update_press_cycle(dt_sec)
        elif self.type == "LASER":
            self._update_laser_cycle(dt_sec)

        # Health sensors
        self._update_health_sensors(dt_sec)

        # Alarms and warnings
        self._check_alarms()
        self._update_warnings()

    # ========================================
    # CNC REALISTIC CYCLE
    # ========================================

    def _update_cnc_cycle(self, dt_sec: float) -> None:
        if self.cyclePhase == "IDLE":
            self._phase_idle(dt_sec)
        elif self.cyclePhase == "SPINDLE_RAMP":
            self._phase_spindle_ramp(dt_sec)
        elif self.cyclePhase == "RAPID":
            self._phase_rapid(dt_sec)
        elif self.cyclePhase == "CUTTING":
            self._phase_cutting(dt_sec)
        elif self.cyclePhase == "RETRACT":
            self._phase_retract(dt_sec)
        elif self.cyclePhase == "DWELL":
            self._phase_dwell(dt_sec)
        elif self.cyclePhase == "FINISH":
            self._phase_finish(dt_sec)

    def _phase_idle(self, dt_sec: float) -> None:
        self.execution = "IDLE"

        # Natural deceleration
        self.spindleSpeed = max(0.0, self.spindleSpeed - 500.0 * dt_sec)
        self.feedRate = max(0.0, self.feedRate - 500.0 * dt_sec)
        self.spindleLoad = max(0.0, self.spindleLoad - 5.0 * dt_sec)

        # Coolant recovery
        if self.coolant is not None:
            self.coolant["level"] = min(100.0, self.coolant["level"] + 0.1)
            self.coolant["flow"] = 0.0

        # Start new cycle (5% chance)
        if random.random() < 0.05:
            self._start_new_cycle()

    def _start_new_cycle(self) -> None:
        self.cyclePhase = "SPINDLE_RAMP"
        self.execution = "RUNNING"
        self.timeInPhase = 0.0
        self.cycleTimeTarget = 20 + random.random() * 25
        self.targetSpindleSpeed = 3000 + random.random() * (self.specs["maxRPM"] - 3000)
        self.targetFeed = 300 + random.random() * 1500

        if not self.programRunning:
            self.programRunning = f"O{random.randint(1000, 9999)}"

    def _phase_spindle_ramp(self, dt_sec: float) -> None:
        self.execution = "RUNNING"
        ramp = 350.0 * dt_sec

        if self.spindleSpeed < self.targetSpindleSpeed:
            self.spindleSpeed += ramp
            if self.spindleSpeed >= self.targetSpindleSpeed:
                self.spindleSpeed = self.targetSpindleSpeed
                self.cyclePhase = "RAPID"
                self.timeInPhase = 0.0

        if self.targetSpindleSpeed > 0:
            self.spindleLoad = min(
                20.0, (self.spindleSpeed / self.targetSpindleSpeed) * 15.0
            )
        self.spindleOrientation = (self.spindleOrientation + self.spindleSpeed * dt_sec / 60.0) % 360.0

    def _phase_rapid(self, dt_sec: float) -> None:
        self.execution = "RUNNING"
        limits = self.specs["axisLimits"]

        # G0: random position
        self.axisPositions["X"] = limits["X"][0] + random.random() * (limits["X"][1] - limits["X"][0])
        self.axisPositions["Y"] = limits["Y"][0] + random.random() * (limits["Y"][1] - limits["Y"][0])
        self.axisPositions["Z"] = limits["Z"][1]

        self.rapidRate = self.specs["rapidTraverse"]
        self.feedRate = 0.0
        self.spindleLoad = 5.0 + random.random() * 5.0

        if self.timeInPhase >= 3.0:
            self.cyclePhase = "CUTTING"
            self.timeInPhase = 0.0

    def _phase_cutting(self, dt_sec: float) -> None:
        self.execution = "RUNNING"

        # Feed ramp-up
        ramp = 200.0 * dt_sec
        if self.feedRate < self.targetFeed:
            self.feedRate += ramp
            if self.feedRate > self.targetFeed:
                self.feedRate = self.targetFeed

        # Z descent
        limits = self.specs["axisLimits"]
        if self.targetFeed > 0:
            self.axisPositions["Z"] -= 1.0 * dt_sec * (self.feedRate / self.targetFeed)
        if self.axisPositions["Z"] < limits["Z"][0] + 5.0:
            self.axisPositions["Z"] = limits["Z"][0] + 5.0

        # Spindle load
        base_load = (self.feedRate / 1800.0) * 35.0
        wear_load = self.toolWear * 50.0
        vib_load = self.vibration * 8.0
        noise = random.random() * 4.5 - 2.0

        self.spindleLoad = max(0.0, min(100.0, base_load + wear_load + vib_load + noise))

        # Tool wear
        self.toolWear += self.spindleLoad / 250000.0
        self.toolWear = min(self.toolWear, 1.0)

        # Vibration
        self.vibration = self.toolWear * 3.0 + random.random() * 0.4

        # Spindle hours
        if self.spindleSpeed > 300.0:
            self.spindleHours += dt_sec / 3600.0

        # Current tool usage
        if self.tools is not None and self.currentTool is not None:
            idx = self.currentTool - 1
            if 0 <= idx < len(self.tools):
                tool = self.tools[idx]
                tool["currentLife"] = max(0.0, tool["currentLife"] - random.random() * 0.02)
                tool["inUse"] = True
                tool["totalCuts"] += 1

        # Coolant consumption
        if self.coolant is not None:
            self.coolant["level"] = max(0.0, self.coolant["level"] - random.random() * 0.08)
            self.coolant["pressure"] = 45.0 + random.random() * 15.0
            self.coolant["temperature"] = 72.0 + random.random() * 15.0
            self.coolant["flow"] = 5.0 + random.random() * 3.0

        # Servo loads
        self.servoLoad["X"] = 20.0 + random.random() * 30.0
        self.servoLoad["Y"] = 20.0 + random.random() * 30.0
        self.servoLoad["Z"] = 30.0 + self.spindleLoad * 0.5

        # Following error simulation
        self.servoFollowingError["X"] = random.random() * 0.002
        self.servoFollowingError["Y"] = random.random() * 0.002
        self.servoFollowingError["Z"] = random.random() * 0.003

        # Cycle completion
        if self.timeInPhase >= self.cycleTimeTarget * 0.6:
            self.cyclePhase = "RETRACT"
            self.timeInPhase = 0.0

    def _phase_retract(self, dt_sec: float) -> None:
        self.execution = "RUNNING"
        limits = self.specs["axisLimits"]

        self.axisPositions["Z"] += 4.0 * dt_sec
        if self.axisPositions["Z"] >= limits["Z"][1] - 10.0:
            self.axisPositions["Z"] = limits["Z"][1] - 10.0
            self.cyclePhase = "DWELL"
            self.timeInPhase = 0.0

        self.spindleLoad = max(5.0, self.spindleLoad - 10.0 * dt_sec)
        self.feedRate = max(0.0, self.feedRate - 300.0 * dt_sec)

    def _phase_dwell(self, dt_sec: float) -> None:
        self.execution = "RUNNING"
        self.feedRate = 0.0
        self.spindleLoad = max(0.0, self.spindleLoad - 5.0 * dt_sec)

        if self.timeInPhase >= 2.0:
            self.cyclePhase = "FINISH"
            self.timeInPhase = 0.0

    def _phase_finish(self, dt_sec: float) -> None:
        self.execution = "RUNNING"
        self.partCount += 1
        self.totalCycles += 1

        self.spindleLoad *= 0.7
        self.feedRate = 0.0

        if self.tools is not None and self.currentTool is not None:
            idx = self.currentTool - 1
            if 0 <= idx < len(self.tools):
                self.tools[idx]["inUse"] = False

        if self.machineOnHours > 0:
            self.productionRate = round(self.partCount / self.machineOnHours)

        self.cyclePhase = "IDLE"
        self.timeInPhase = 0.0

    # ========================================
    # PRESS BRAKE CYCLE
    # ========================================

    def _update_press_cycle(self, dt_sec: float) -> None:
        if self.cyclePhase == "IDLE" and random.random() < 0.05:
            self.cyclePhase = "RUNNING"
            self.execution = "RUNNING"
            self.timeInPhase = 0.0
            self.bendAngle = 45.0 + random.random() * 90.0

        if self.cyclePhase == "RUNNING":
            self.execution = "RUNNING"
            self.ramPosition = min(100.0, self.ramPosition + 20.0 * dt_sec)
            self.tonnage = (self.ramPosition / 100.0) * (self.maxTonnage * 0.8)
            self.spindleLoad = (self.tonnage / self.maxTonnage) * 100.0
            self.servoLoad["Y"] = self.tonnage / self.maxTonnage * 80.0

            if self.timeInPhase >= 5.0:
                self.partCount += 1
                self.totalCycles += 1
                self.ramPosition = 0.0
                self.tonnage = 0.0
                self.cyclePhase = "IDLE"
                self.execution = "IDLE"
                self.timeInPhase = 0.0
        else:
            self.execution = "IDLE"
            self.spindleLoad = 0.0
            self.tonnage = 0.0

    # ========================================
    # LASER CYCLE
    # ========================================

    def _update_laser_cycle(self, dt_sec: float) -> None:
        if self.cyclePhase == "IDLE" and random.random() < 0.07:
            self.cyclePhase = "RUNNING"
            self.execution = "RUNNING"
            self.timeInPhase = 0.0
            self.laserPower = 2000.0 + random.random() * (self.maxLaserPower - 2000.0)
            self.targetFeed = 800.0 + random.random() * 2200.0

        if self.cyclePhase == "RUNNING":
            self.execution = "RUNNING"
            self.spindleLoad = (self.laserPower / self.maxLaserPower) * 100.0

            if self.cutSpeed < self.targetFeed:
                self.cutSpeed += 300.0 * dt_sec
                if self.cutSpeed > self.targetFeed:
                    self.cutSpeed = self.targetFeed

            self.feedRate = self.cutSpeed

            self.axisPositions["X"] += random.random() * 10.0 - 5.0
            self.axisPositions["Y"] += random.random() * 10.0 - 5.0

            self.resonatorTemp += (self.laserPower / self.maxLaserPower) * 0.4

            if self.timeInPhase >= 8.0:
                self.partCount += 1
                self.totalCycles += 1
                self.cyclePhase = "IDLE"
                self.execution = "IDLE"
                self.timeInPhase = 0.0
                self.cutSpeed = 0.0
                self.feedRate = 0.0
        else:
            self.execution = "IDLE"
            self.spindleLoad = 0.0
            self.cutSpeed = 0.0
            self.feedRate = 0.0
            self.resonatorTemp = max(26.0, self.resonatorTemp - 0.05)

    # ========================================
    # HEALTH SENSORS
    # ========================================

    def _update_health_sensors(self, dt_sec: float) -> None:
        if self.execution == "RUNNING":
            self.temperature = min(120.0, self.temperature + (self.spindleLoad / 100.0) * 0.3)
            self.spindleTemp = min(95.0, self.spindleTemp + (self.spindleLoad / 100.0) * 0.15)
            self.currentAmps = 7.0 + (self.spindleLoad / 100.0) * 8.0
        else:
            self.temperature = max(72.0, self.temperature - 0.2)
            self.spindleTemp = max(25.0, self.spindleTemp - 0.03)
            self.currentAmps = max(7.0, self.currentAmps - 0.5)

        # Battery drain (very slow)
        self.batteryVoltage -= 0.0001 * dt_sec
        if self.batteryVoltage < 2.8:
            self.batteryVoltage = 2.8

        # Oil system
        self.oilPressure = 45.0 + random.random() * 10.0
        self.oilLevel = max(20.0, self.oilLevel - 0.001)

        # Servo temperatures
        if self.execution == "RUNNING":
            for axis in ("X", "Y", "Z"):
                self.servoTemp[axis] = min(65.0, self.servoTemp[axis] + 0.1)
        else:
            for axis in ("X", "Y", "Z"):
                self.servoTemp[axis] = max(25.0, self.servoTemp[axis] - 0.05)

    # ========================================
    # ALARM SYSTEM
    # ========================================

    def _check_alarms(self) -> None:
        if self.type in ("CNC_MILL", "LATHE"):
            # Axis following error
            if self.servoFollowingError["X"] > 0.005 and random.random() < 0.02:
                self._set_alarm(103, "X AXIS FOLLOWING ERROR")
            elif self.servoFollowingError["Y"] > 0.005 and random.random() < 0.02:
                self._set_alarm(104, "Y AXIS FOLLOWING ERROR")
            elif self.servoFollowingError["Z"] > 0.005 and random.random() < 0.02:
                self._set_alarm(105, "Z AXIS FOLLOWING ERROR")
            # Low battery
            elif self.batteryVoltage < 3.0 and random.random() < 0.05:
                self._set_alarm(9100, "LOW BATTERY")
            # Coolant pump fault
            elif self.coolant is not None and self.coolant["level"] < 10.0 and random.random() < 0.1:
                self._set_alarm(115, "COOLANT PUMP FAULT")
            # Spindle overload
            elif self.spindleLoad > 95.0 and random.random() < 0.05:
                self._set_alarm(None, "SPINDLE_OVERLOAD")
            # High temperature
            elif self.spindleTemp > 85.0 and random.random() < 0.08:
                self._set_alarm(200, "SPINDLE OVER TEMP")
            # Tool life expired
            elif self.tools is not None and self.currentTool is not None:
                idx = self.currentTool - 1
                if 0 <= idx < len(self.tools):
                    tool = self.tools[idx]
                    if tool["currentLife"] < 5.0 and random.random() < 0.15:
                        self._set_alarm(None, "TOOL_LIFE_EXPIRED")
            # High vibration
            elif self.vibration > 5.0 and random.random() < 0.08:
                self._set_alarm(None, "HIGH_VIBRATION")

        if self.type == "PRESS_BRAKE":
            if self.tonnage > self.maxTonnage * 0.9 and random.random() < 0.1:
                self._set_alarm(None, "OVER_TONNAGE")

        if self.type == "LASER":
            if self.spindleLoad > 95.0 and random.random() < 0.1:
                self._set_alarm(None, "LASER_POWER_FAULT")
            if self.resonatorTemp > 85.0 and random.random() < 0.08:
                self._set_alarm(None, "RESONATOR_OVERHEAT")

    def _set_alarm(self, code: Optional[int], message: str) -> None:
        self.alarm = message
        self.alarmCode = code
        self.alarmHistory.append(
            {
                "code": code,
                "message": message,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "cyclePhase": self.cyclePhase,
                "spindleLoad": self.spindleLoad,
                "cleared": False,
            }
        )
        # Keep last 20
        if len(self.alarmHistory) > 20:
            self.alarmHistory = self.alarmHistory[-20:]

    def _clear_alarm(self) -> None:
        if self.alarmHistory:
            self.alarmHistory[-1]["cleared"] = True
        self.alarm = None
        self.alarmCode = None
        self.execution = "IDLE"

    # ========================================
    # WARNING SYSTEM
    # ========================================

    def _update_warnings(self) -> None:
        self.warnings = []

        if self.batteryVoltage < 3.2:
            self.warnings.append(
                {"type": "BATTERY_LOW", "severity": "warning", "message": "Battery voltage low"}
            )

        if self.coolant is not None and self.coolant["level"] < 20.0:
            self.warnings.append(
                {"type": "COOLANT_LOW", "severity": "warning", "message": "Coolant level below 20%"}
            )

        if self.tools is not None and self.currentTool is not None:
            idx = self.currentTool - 1
            if 0 <= idx < len(self.tools):
                tool = self.tools[idx]
                if tool["currentLife"] < 15.0:
                    self.warnings.append(
                        {
                            "type": "TOOL_WEAR",
                            "severity": "warning",
                            "message": f"Tool {self.currentTool} life below 15%",
                        }
                    )

        if self.spindleTemp > 75.0:
            self.warnings.append(
                {"type": "HIGH_TEMP", "severity": "warning", "message": "Spindle temperature elevated"}
            )

        if self.spindleLoad > 85.0:
            self.warnings.append(
                {"type": "HIGH_LOAD", "severity": "caution", "message": "Spindle load above 85%"}
            )

    # ========================================
    # MANUAL CONTROLS
    # ========================================

    def set_power(self, state: bool) -> None:
        self.power = state
        if not state:
            self.execution = "STOPPED"
            self.cyclePhase = "IDLE"

    def inject_alarm(self, code: Optional[int], message: str) -> None:
        self._set_alarm(code, message)

    def clear_alarm(self) -> None:
        self._clear_alarm()

    # ========================================
    # JSON / DICT OUTPUT
    # ========================================

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "type": self.type,
            "specs": self.specs,
            "power": self.power,
            "execution": self.execution,
            "cyclePhase": self.cyclePhase,
            "alarm": self.alarm,
            "alarmCode": self.alarmCode,
            "alarmHistory": self.alarmHistory[-5:],  # last 5
            "warnings": self.warnings,
            "spindleSpeed": round(self.spindleSpeed),
            "spindleLoad": round(self.spindleLoad, 1),
            "spindleTemp": round(self.spindleTemp, 1),
            "spindleHours": round(self.spindleHours, 3),
            "spindleOrientation": round(self.spindleOrientation),
            "feedRate": round(self.feedRate),
            "rapidRate": round(self.rapidRate),
            "axisPositions": {
                "X": round(self.axisPositions["X"], 2),
                "Y": round(self.axisPositions["Y"], 2),
                "Z": round(self.axisPositions["Z"], 2),
            },
            "servoLoad": self.servoLoad,
            "servoFollowingError": self.servoFollowingError,
            "servoTemp": self.servoTemp,
            "partCount": self.partCount,
            "totalCycles": self.totalCycles,
            "machineOnHours": round(self.machineOnHours, 3),
            "productionRate": self.productionRate,
            "batteryVoltage": round(self.batteryVoltage, 2),
            "temperature": round(self.temperature),
            "vibration": round(self.vibration, 2),
            "currentAmps": round(self.currentAmps, 1),
            "oilPressure": round(self.oilPressure),
            "oilLevel": round(self.oilLevel),
            "timestamp": self.timestamp.isoformat() + "Z",
        }

        if self.type in ("CNC_MILL", "LATHE"):
            data["currentTool"] = self.currentTool
            data["tools"] = self.tools
            data["toolChangeCount"] = self.toolChangeCount
            data["toolWear"] = round(self.toolWear, 3)
            data["coolant"] = self.coolant

        if self.type == "PRESS_BRAKE":
            data["tonnage"] = round(self.tonnage)
            data["maxTonnage"] = self.maxTonnage
            data["ramPosition"] = round(self.ramPosition)
            data["backGauge"] = self.backGauge
            data["bendAngle"] = round(self.bendAngle)

        if self.type == "LASER":
            data["laserPower"] = round(self.laserPower)
            data["maxLaserPower"] = self.maxLaserPower
            data["gasPressure"] = round(self.gasPressure)
            data["resonatorTemp"] = round(self.resonatorTemp, 1)
            data["cutSpeed"] = round(self.cutSpeed)

        if self.material is not None:
            data["material"] = self.material
        if self.programRunning is not None:
            data["programRunning"] = self.programRunning

        return data

# ========================================
# FACTORY: 6 MACHINES WE'VE BEEN USING
# ========================================

def create_default_machines() -> Dict[str, HaasMachine]:
    machines: Dict[str, HaasMachine] = {}

    # 1) Haas VF-2 - small vertical mill
    machines["haas_vf2"] = HaasMachine(
        machine_id="haas_vf2",
        name="Haas VF-2",
        model="VF-2",
        mtype="CNC_MILL",
        specs={
            "axisLimits": {"X": (0.0, 762.0), "Y": (0.0, 406.0), "Z": (0.0, 508.0)},
            "spindlePower": 30,
            "maxRPM": 8100,
            "rapidTraverse": 1000,
            "toolCapacity": 24,
        },
    )

    # 2) Haas VF-4 - larger mill
    machines["haas_vf4"] = HaasMachine(
        machine_id="haas_vf4",
        name="Haas VF-4",
        model="VF-4",
        mtype="CNC_MILL",
        specs={
            "axisLimits": {"X": (0.0, 1270.0), "Y": (0.0, 508.0), "Z": (0.0, 635.0)},
            "spindlePower": 30,
            "maxRPM": 8100,
            "rapidTraverse": 900,
            "toolCapacity": 30,
        },
    )

    # 3) Toyoda HMC
    machines["toyoda_hmc"] = HaasMachine(
        machine_id="toyoda_hmc",
        name="Toyoda HMC",
        model="HMC",
        mtype="CNC_MILL",
        specs={
            "axisLimits": {"X": (0.0, 800.0), "Y": (0.0, 800.0), "Z": (0.0, 800.0)},
            "spindlePower": 40,
            "maxRPM": 12000,
            "rapidTraverse": 1200,
            "toolCapacity": 60,
        },
    )

    # 4) CNC Lathe
    machines["cnc_lathe"] = HaasMachine(
        machine_id="cnc_lathe",
        name="CNC Lathe",
        model="ST-20",
        mtype="LATHE",
        specs={
            "axisLimits": {"X": (0.0, 300.0), "Y": (0.0, 0.0), "Z": (0.0, 600.0)},
            "spindlePower": 20,
            "maxRPM": 4000,
            "rapidTraverse": 800,
            "toolCapacity": 12,
        },
    )

    # 5) Press Brake
    machines["press_brake"] = HaasMachine(
        machine_id="press_brake",
        name="Press Brake 200T",
        model="PRESS",
        mtype="PRESS_BRAKE",
        specs={
            "axisLimits": {"X": (0.0, 3000.0), "Y": (0.0, 0.0), "Z": (0.0, 1000.0)},
            "maxTonnage": 200,
        },
    )

    # 6) Laser Cutter
    machines["laser_cut"] = HaasMachine(
        machine_id="laser_cut",
        name="Fiber Laser 6kW",
        model="LASER",
        mtype="LASER",
        specs={
            "axisLimits": {"X": (0.0, 3000.0), "Y": (0.0, 1500.0), "Z": (0.0, 200.0)},
            "maxLaserPower": 6000,
        },
    )

    return machines

# ========================================
# SIMPLE LOCAL LOOP (for quick testing)
# ========================================

if __name__ == "__main__":
    import json
    import time

    machines = create_default_machines()

    print("Starting local Haas simulator (Python) with 6 machines...")
    try:
        while True:
            for m in machines.values():
                m.update(1.0)  # 1 second step
                print(json.dumps(m.to_dict()))
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("Simulator stopped.")
