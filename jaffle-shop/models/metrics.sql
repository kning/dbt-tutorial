select * 
from {{ metrics.calculate(
    metric('count_trips'),
    grain='day'
) }}
