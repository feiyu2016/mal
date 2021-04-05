#OPTS_GC := -XX:+UseConcMarkSweepGC -verbose:gc -Xms20M -Xmx20M -Xmn10M -XX:+PrintGCDetails -XX:SurvivorRatio=8
OPTS_GC := -XX:+UseSerialGC -verbose:gc -Xms20M -Xmx20M -Xmn10M -XX:+PrintGCDetails -XX:SurvivorRatio=8

gc37:
	# P130
	# 分配allocation4时，发生一次Minor GC，这次回收的结果是，新生代
	# 6651K -> 148K，而总内存占用量几乎没有减少（因为allocation1, allocation2, allocation3都是
	# 存活的，虚拟机几乎没有找到可以回收的对象）。
	# 产生这次GC的原因，是为allocation4分配内存时，发现Eden已经被占用了6MB，剩余空间
	# 已不足以分配allocation4所需的4M内存，因此发生Minor GC。GC期间，虚拟机发现已有的三个
	# 2M大小的对象无法放入Survivor空间（Survivor空间只有1M大小），所以只好通过分配担保
	# 机制提前转移到老年代去。P79
	javac GC37.java
	java $(OPTS_GC) GC37

gc38:
	# P131
	# 大对象直接进入老年代
	javac GC38.java
	java $(OPTS_GC) -XX:PretenureSizeThreshold=3145728 GC38