public interface Lifecycle {  
  void start();  
  void stop();  
  boolean isRunning();  
}

public interface LifecycleProcessor extends Lifecycle {  
  void onRefresh();  
  void onClose();  
}

public interface Phased {  
  int getPhase();  
}

public interface SmartLifecycle extends Lifecycle, Phased {  
  boolean isAutoStartup();  
  void stop(Runnable callback);  
}  
