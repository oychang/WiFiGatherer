set datafile separator ","
plot 'network_density.csv' u 2:1:(1.2*log(column(3))) w points lt 1 pt 6 ps variable

