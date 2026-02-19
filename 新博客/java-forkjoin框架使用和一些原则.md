# 先扯一波使用 两个demo解决


1. 使用RecursiveAction无状态任务拆分(无返回值状态)

注意几个点

- awaitQuiescence 是监控这个forkjoin是否都完成
- awaitTermination 是监控这个forkjoin是否shutdown
- 使用execute表示用无返回值的方法来处理异步请求

```java
public class TestForkJoin {
    public static void main(String[] args) throws InterruptedException {
        ForkJoinPool forkJoinPool = new ForkJoinPool(8);
        MyRecursiveAction myRecursiveAction = new MyRecursiveAction(new int[]{
                1,2,3,4,5,6,7,8,9
        },0,8);
        forkJoinPool.execute(myRecursiveAction);
        //阻塞当前线程直到 ForkJoinPool 中所有的任务都执行结束
        // awaitQuiescence 阻塞判断当前的线程是否都是完成的
        while(!forkJoinPool.awaitQuiescence(50,TimeUnit.NANOSECONDS)){

        }
        forkJoinPool.shutdown();
        forkJoinPool.awaitTermination(50,TimeUnit.DAYS);
        System.out.println("nb");
    }
}

class MyRecursiveAction extends RecursiveAction{
    private int[] itemList;
    private int start;
    private int end;

    public MyRecursiveAction(int[] itemList,int start,int end){
        this.itemList = itemList;
        this.start = start;
        this.end = end;
    }
    /**
     * The main computation performed by this task.
     */
    @Override
    protected void compute() {
        if(start>end){
            return;
        }
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        if(end+1-start>3){
            MyRecursiveAction recursiveAction = new MyRecursiveAction(itemList,start,start+2);
            MyRecursiveAction recursiveAction2 = new MyRecursiveAction(itemList,start+3,end);
            recursiveAction.fork();
            System.out.println("one end");
            recursiveAction2.fork();
            System.out.println("two end");
        }else{
            while(start<=end){
                System.out.print(itemList[start]+" ");
                start++;
            }
            System.out.println();
        }
    }
}
```

2. 使用RecursiveTask有状态任务查分

注意一个点

使用 submit 和 future类来实现监控返回值状态


```java
public class TestForkJoin {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        ForkJoinPool forkJoinPool = new ForkJoinPool(8);
        MyRecursiveTask myRecursiveAction = new MyRecursiveTask(new int[] {
                1, 2, 3, 4, 5, 6, 7, 8, 9
        }, 0, 8);
        Future<Integer> item = forkJoinPool.submit(myRecursiveAction);
        System.out.println(item.get());
    }
}

class MyRecursiveTask extends RecursiveTask<Integer> {

    private int[] itemList;
    private int start;
    private int end;

    public MyRecursiveTask(int[] itemList, int start, int end) {
        this.itemList = itemList;
        this.start = start;
        this.end = end;
    }

    @Override
    protected Integer compute() {
        if(start==end){
            return itemList[start];
        }
        MyRecursiveTask left = new MyRecursiveTask(itemList,start,(start+end)/2);
        MyRecursiveTask right = new MyRecursiveTask(itemList,(start+end)/2+1,end);
        invokeAll(left,right);
        return left.join()+right.join();
    }
}
```

# 原理这里就不说了 , 主要是几个特性

1. 自动的线程扩展
    - 很多线程池都有这种能力,通过监控cpu核心数量来创建线程数量
2. 工作窃取
    - 空闲的线程去窃取其他工作线程队列中的任务 类似WorkStealingPool 多工作队列线程池
3. 任务分片
    - forkjoin框架的核心