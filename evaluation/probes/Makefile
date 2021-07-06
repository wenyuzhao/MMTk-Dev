include common.mk

JAVAC=/usr/lib/jvm/java-6-openjdk-amd64/bin/javac
#usage: make [OPTION=-m32]. If OPTION=-m32 is specified and the current machine is X86_64, 32bit version will be build.
#Before run make:
#1) Please set the JDK variable in common.mk.
#2) Install libpfm (http://perfmon2.sourceforge.net).
#3) Download dacapo-2006-10-MR2 (https://sourceforge.net/projects/dacapobench/files/archive/2006-10-MR2/), and copy it to ${BENCHMARKS}
#4) Download dacapo-9.12-MR1-bach.jar (https://sourceforge.net/projects/dacapobench/files/9.12-bach-MR1/), and copy it to ${BENCHMARKS}

all: native-code probes.jar

##	cd native/valgrind; $(MAKE) $(MFLAGS) all
#	cp -a native/valgrind/libvalgrind.so libvalgrind.so
native-code:
	cd native/rust_mmtk; $(MAKE) $(MFLAGS) all
	cp -a native/rust_mmtk/librust_mmtk_probe.so librust_mmtk_probe.so
	cp -a native/rust_mmtk/librust_mmtk_probe_32.so librust_mmtk_probe_32.so
	cd native/hello_world; $(MAKE) $(MFLAGS) all
	cp -a native/hello_world/libhello_world.so libhello_world.so
	cd native/perf_event; $(MAKE) $(MFLAGS) all
	cp -a native/perf_event/perf_event_launcher perf_event_launcher
	cp -a native/perf_event/libperf_event_launcher.so libperf_event_launcher.so
	cp -a native/perf_event/libperf_event_reader.so libperf_event_reader.so
	cd native/ptlsim; $(MAKE) $(MFLAGS) all
	cp -a native/ptlsim/libptlsim.so libptlsim.so


test: all
	$(JAVA) -Djava.library.path=`pwd` -Dprobes=HelloWorldNative -cp probes.jar:$(DACAPO2006JAR) Harness -c probe.Dacapo2006Callback fop
	$(JAVA) -Dprobes=HelloWorld -cp probes.jar:$(DACAPO2006JAR) Harness -c probe.Dacapo2006Callback fop
	$(JAVA) -Dprobes=Scenario -cp probes.jar:$(DACAPOBACHJAR) Harness -c probe.DacapoBachCallback fop
	$(JAVA) -Dprobes=Scenario -cp probes.jar:$(DACAPOCHOPINJAR) Harness -c probe.DacapoChopinCallback fop
	cd /usr/share/benchmarks/SPECjvm98; $(JAVA) -Dprobes=HelloWorld -cp $(CURDIR)/probes.jar:. SpecApplication -i1 _202_jess
	$(JAVA) -Xmx1G -Xms200M -Dprobes=HelloWorld -cp probes.jar:/usr/share/benchmarks/pjbb2005/jbb.jar:/usr/share/benchmarks/pjbb2005/check.jar spec.jbb.JBBmain -propfile SPECjbb-8x10000.props -c probe.PJBB2005Callback -n 1
	./perf_event_launcher PERF_COUNT_HW_CPU_CYCLES,PERF_COUNT_HW_INSTRUCTIONS $(JAVA) -Djava.library.path=`pwd` -Dprobes=PerfEventLauncher -cp probes.jar:$(DACAPO2006JAR) Harness -c probe.Dacapo2006Callback fop
	./perf_event_launcher PERF_COUNT_HW_CPU_CYCLES $(JAVA) -Djava.library.path=`pwd` -Dprobes=PerfEventLauncher -cp probes.jar:$(DACAPOBACHJAR) Harness -c probe.DacapoBachCallback fop
	$(JAVA) -Djava.library.path=`pwd` -Dprobes=PTLsim -cp probes.jar:$(DACAPO2006JAR) Harness -c probe.Dacapo2006Callback fop
	$(JAVA) -Djava.library.path=`pwd` -Dprobes=Valgrind -cp probes.jar:$(DACAPO2006JAR) Harness -c probe.Dacapo2006Callback fop
	$(JAVA) -Djava.library.path=`pwd` -Dprobes=StopJIT -Dprobe.stopjit.sleeptime=3 -Dprobe.stopjit.iteration=4 -cp probes.jar:$(DACAPO2006JAR) Harness -c probe.Dacapo2006Callback -n 5 fop


clean:
	rm -f *.so
	rm -f *.class
	rm -f *.jar
	rm -f spec/harness/*.class
	rm -f probe/*.class
	cd native/perf_event; $(MAKE) $(MFLAGS) clean
	cd native/hello_world; $(MAKE) $(MFLAGS) clean
	cd native/ptlsim; $(MAKE) $(MFLAGS) clean
	cd native/valgrind; $(MAKE) $(MFLAGS) clean

probes.jar: probe/RustMMTkProbe.class probe/RustMMTk32Probe.class probe/OpenJDKProbe.class probe/HelloWorldNativeProbe.class probe/ScenarioProbe.class probe/StopJITProbe.class probe/ValgrindProbe.class probe/PTLsimProbe.class probe/JikesRVMPerfEventProbe.class probe/MMTkProbe.class probe/ThreadEventProbe.class probe/PowerProbe.class probe/PerfEventProbe.class probe/PerfEventReader.class probe/PerfEventLauncherProbe.class probe/ApplicationPerfEventProbe.class probe/HelloWorldProbe.class probe/Probe.class probe/ProbeMux.class probe/Dacapo2006Callback.class probe/DacapoBachCallback.class probe/DacapoChopinCallback.class spec/harness/ProgramRunner.class spec/harness/RunProgram.class SpecApplication.class probe/ReplayProbe.class probe/CompilerSamplesProbe.class probe/PJBB2005Callback.class
	zip -r probes.jar *.class spec/harness/*.class probe/*.class
	zip -r probes.jar *.class probe/*.class

probe/RustMMTk32Probe.class: probe/RustMMTk32Probe.java
	$(JAVAC) -target 1.6 -cp . $<

SpecApplication.class: SpecApplication.java
	$(JAVAC) -implicit:none -cp .:/usr/share/benchmarks/SPECjvm98 -sourcepath . $<

spec/%.class: spec/%.java
	$(JAVAC) -implicit:none -cp .:/usr/share/benchmarks/SPECjvm98 -sourcepath . $<

%.class: %.java
	$(JAVAC) -cp . $<

probe/Dacapo2006Callback.class:
	$(JAVAC) -cp .:$(DACAPO2006JAR) probe/Dacapo2006Callback.java

probe/DacapoBachCallback.class:
	$(JAVAC) -cp .:$(DACAPOBACHJAR) probe/DacapoBachCallback.java

probe/DacapoChopinCallback.class:
	$(JDK)/bin/javac -cp .:$(DACAPOCHOPINJAR) probe/DacapoChopinCallback.java

probe/PJBB2005Callback.class:
	$(JAVAC) -cp .:/usr/share/benchmarks/pjbb2005/jbb.jar probe/PJBB2005Callback.java

probe/OpenJDKProbe.class: probe/OpenJDKProbe.java
	$(JAVAC) -cp . probe/OpenJDKProbe.java

probe/RustMMTkProbe.class: probe/RustMMTkProbe.java
	$(JAVAC) -cp . probe/RustMMTkProbe.java
