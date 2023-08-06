import statistics_viz as statsviz

stats = statsviz.StatisticsCollector(["pepe", "poop", "# pak"])


stats.add((1, 2.1, 23.3))
stats.add((1, 2.1, 23.3))
stats.add((1, 2.1, 23.3))
stats.add((1, 2.1, 23.3))
stats.add((1, 2.1, 23.3))
stats.plot(["pepe"])
