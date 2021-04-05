#OPTS_GC := -XX:+UseConcMarkSweepGC -verbose:gc -Xms20M -Xmx20M -Xmn10M -XX:+PrintGCDetails -XX:SurvivorRatio=8
OPTS_GC := -XX:+UseSerialGC -verbose:gc -Xms20M -Xmx20M -Xmn10M -XX:+PrintGCDetails -XX:SurvivorRatio=8

gc37:
	javac GC37.java
	java $(OPTS_GC) GC37

gc38:
	javac GC38.java
	java $(OPTS_GC) -XX:PretenureSizeThreshold=3145728 GC38