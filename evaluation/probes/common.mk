JDK=/usr/lib/jvm/default-java
JAVAC=$(JDK)/bin/javac
JAVA=$(JDK)/bin/java
BENCHMARKS=/usr/share/benchmarks
DACAPO2006JAR=$(BENCHMARKS)/dacapo/dacapo-2006-10-MR2.jar
DACAPOBACHJAR=$(BENCHMARKS)/dacapo/dacapo-9.12-bach.jar
DACAPOCHOPINJAR=$(BENCHMARKS)/dacapo/dacapo-evaluation-git-69a704e.jar
CFLAGS=-O2 -g -Wall -Werror -D_GNU_SOURCE -fPIC
ifeq (-m32,$(findstring -m32,$(OPTION)))
M32_FLAG = y
CFLAGS += -m32
endif
