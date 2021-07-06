package probe;

import org.dacapo.harness.Callback;
import org.dacapo.harness.CommandLineArgs;

public class DacapoChopinCallback extends Callback {
  public DacapoChopinCallback(CommandLineArgs cla) {
    super(cla);
    ProbeMux.init();
  }

  public void start(String benchmark) {
    ProbeMux.begin(benchmark, isWarmup());
    super.start(benchmark);
  };

  /* Immediately after the end of the benchmark */
  public void stop(long duration) {
    super.stop(duration);
    ProbeMux.end(isWarmup());
    if (!isWarmup()) {
      ProbeMux.cleanup();
    }
  }
}
