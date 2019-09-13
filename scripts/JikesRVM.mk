
DACAPO ?= lusearch
HEAP ?= 500M
GC ?= production

MACHINE ?= elk.moma
DACAPO_VERSION ?= 9.12
N ?= 1
# GC_THREADS = 1

# Constants

LOCAL_HOME = /home/wenyu
REMOTE_HOME = /home/wenyuz
LOG_DIR = ../logs
JIKESRVM_ROOT = Projects/JikesRVM-Rust

# Derived Variables

SSH_PREFIX = ssh $(MACHINE) -t RUST_BACKTRACE=1
RVM = $(JIKESRVM_ROOT)/dist/$(GC)_x86_64-linux/rvm
DACAPO_JAR = /usr/share/benchmarks/dacapo/dacapo-$(DACAPO_VERSION)-bach.jar
RVM_ARGS = $(if $(GC_THREADS), -X:gc:threads=$(GC_THREADS)) -Xms$(HEAP) -Xmx$(HEAP) -X:gc:variableSizeHeap=false -server -jar $(DACAPO_JAR) $(DACAPO)



build:
    ifdef NUKE
		@cd $(LOCAL_HOME)/$(JIKESRVM_ROOT) && ./bin/buildit $(MACHINE) $(GC) -j /usr/lib/jvm/java-8-openjdk-amd64 --answer-yes --nuke
    else
		@cd $(LOCAL_HOME)/$(JIKESRVM_ROOT) && ./bin/buildit $(MACHINE) $(GC) -j /usr/lib/jvm/java-8-openjdk-amd64 --answer-yes
    endif

run:
	@for i in $$(seq -w 001 $(N)); do \
       make run-once-impl --no-print-directory log_id=$$i; \
    done

run-once:
	@make run-once-impl --no-print-directory

run-once-impl:
    ifeq ($(or $(log_id), 001), 001)
		@mkdir -p $(LOG_DIR)
        ifeq ($(MACHINE), localhost)
			@echo $(LOCAL_HOME)/$(RVM) $(RVM_ARGS)
  	    else
			@echo $(SSH_PREFIX) $(REMOTE_HOME)/$(RVM) $(RVM_ARGS)
        endif
    endif
    ifeq ($(MACHINE), localhost)
		@trap 'exit' INT && $(LOCAL_HOME)/$(RVM) $(RVM_ARGS) > $(LOG_DIR)/$(or $(log_id),001).log 2>&1; EXIT=$$? $(MAKE) print-result
    else
		@trap 'exit' INT && $(SSH_PREFIX) $(REMOTE_HOME)/$(RVM) $(RVM_ARGS) > $(LOG_DIR)/$(or $(log_id),001).log 2>&1; EXIT=$$? make print-result
    endif

RED='\033[0;31m'
GREEN='\033[0;32m'
RESET='\033[0m' # No Color
print-result:
    ifeq ($(EXIT), 0)
		@echo === '#'$(or $(log_id),001) passed ===
    else
		@echo === '#'$(or $(log_id),001) ${RED}FAILED!!!${RESET} ===
    endif

download:
	scp $(MACHINE):$(FILE) ../$(notdir $(FILE))