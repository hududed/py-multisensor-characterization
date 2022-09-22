from src.PTC10Control import PTC10Control
from src.EZTControl import EZTControl
from src.IET7600PlusControl import IET7600Plus

# ptc10 = PTC10Control('169.254.106.13')
# ezt = EZTControl('169.254.106.15')
iet = IET7600Plus()

# normal params
iet.set_frequency(500)
iet.set_primary_param('CS')
iet.set_num_avg(1)

# sweep params
# iet.sweep_enable('OFF')