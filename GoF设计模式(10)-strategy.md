### 策略模式

这个模式和bridge 模式非常像，如果说区别可能就是bridge强调的是扩展性而stragtegy强调使用方法

### 策略模式类图

![](blogimg/GAF/10.png)

### 策略模式例子

#### context 策略的使用者

```java
package org.kys.Gaf.strategy;

public class PlayerContext {
    private String name;
    private Strategy strategy;
    private int wincount=0;
    private int losecount=0;
    private int gamecount=0;

    public PlayerContext(String name, Strategy strategy) {
        this.name = name;
        this.strategy = strategy;
    }

    public Hand nextHand(){
        return strategy.nextHand();
    }

    public void win(){
        strategy.study(true);
        gamecount++;
        wincount++;
    }
    public void lose(){
        strategy.study(false);
        gamecount++;
        losecount++;
    }

    public void even(){
        gamecount++;
    }
    public double winRate(){
        return (double)wincount/(double) gamecount;
    }
    public String getHandName(){
        return strategy.getHandName();
    }
}

```

#### strategy 定义的策略接口

```java
package org.kys.Gaf.strategy;

public interface Strategy {
    void study(boolean win);
    Hand nextHand();
    String getHandName();
}

```

#### 策略接口的实现类

```java
package org.kys.Gaf.strategy;

import java.util.Random;

/**
 * 学习自身的
 */
public class ProbStrategy implements Strategy{

    private int[][] recording={
            {1,1,1},{1,1,1},{1,1,1}
    };

    private int preValue=1;
    private int currentValue=1;
    private int handvalue=1;
    @Override
    public void study(boolean win) {
        if(win){
            recording[preValue][currentValue]++;
        }else{
            recording[preValue][(currentValue+1)%3]++;
            recording[preValue][(currentValue+2)%3]++;
        }
    }

    private static Random random = new Random();
    
    @Override
    public Hand nextHand() {
        int allSum = 0;
        for (int a=0;a<3;a++){
            allSum+=recording[currentValue][a];
        }
        int ran = random.nextInt(allSum);
        if(ran<recording[currentValue][0]){
            handvalue=0;
        }else if(ran<recording[currentValue][0]+recording[currentValue][1]){
            handvalue=1;
        }else {
            handvalue=2;
        }
        preValue=currentValue;
        currentValue=handvalue;
        return Hand.getHand(handvalue);
    }

    @Override
    public String getHandName() {
        return Hand.getHand(handvalue).getName();
    }
}
```

```java
package org.kys.Gaf.strategy;

import java.util.Random;

public class SimpleStrategy implements Strategy {

    private boolean win = true;
    private int preHandValue = 0;

    @Override
    public void study(boolean win) {
        this.win = win;
    }

    @Override
    public Hand nextHand() {
        this.preHandValue = new Random().nextInt(3);
        return Hand.getHand(preHandValue);
    }

    @Override
    public String getHandName() {
        return Hand.getHand(preHandValue).getName();
    }
}
```

#### 策略的数据载体

```java
package org.kys.Gaf.strategy;

public class Hand {
    public static final int HANDVALUE_GUU = 0;
    public static final int HANDVALUE_GHO = 1;
    public static final int HANDVALUE_PAA = 2;
    public static final Hand[] head = {
            new Hand(HANDVALUE_GUU),
            new Hand(HANDVALUE_GHO),
            new Hand(HANDVALUE_PAA)
    };

    public static final int WIN = 1;
    public static final int LOST = 2;
    public static final int EVEN = 3;

    private final int HANDVALUE;

    private String[] name={
            "石头","剪刀","布"
    };

    public String getName(){
        return name[this.HANDVALUE];
    }

    public Hand(int HANDVALUE){
      this.HANDVALUE=HANDVALUE;
    }

    public static Hand getHand(int handValue){
        return head[handValue];
    }

    public int getHandValue(){
        return this.HANDVALUE;
    }

    public int iswin(Hand hand){
        if(this.HANDVALUE==hand.getHandValue()){
            return EVEN;//平
        }else if(this.HANDVALUE+1%3==hand.getHandValue()){
            return WIN;//胜
        }else{
            return LOST;
        }
    }
}
```

#### 主函数

```java
package org.kys.Gaf.strategy;

import java.util.Random;

public class Main {
    public static void main(String[] args) {
        PlayerContext player1= new PlayerContext("tom",new SimpleStrategy());
        PlayerContext player2 = new PlayerContext("jack",new SimpleStrategy());
                //new PlayerContext("jack",new ProbStrategy());
        for(int a=0;a<10000;a++){
            Hand player1Hand = player1.nextHand();
            Hand player2Hand = player2.nextHand();
            if(player1Hand.iswin(player2Hand)== Hand.WIN){
                player1.win();
                player2.lose();
                System.out.println("palyer1胜  tom:"+player1.getHandName()+" | jack:"+player2.getHandName());
            }else if(player1Hand.iswin(player2Hand)== Hand.LOST){
                player1.lose();
                player2.win();
                System.out.println("palyer2胜  tom:"+player1.getHandName()+" | jack:"+player2.getHandName());
            }else{
                player1.even();
                player2.even();
                System.out.println("player 平  tom:"+player1.getHandName()+" | jack:"+player2.getHandName());
            }
        }
        System.out.println("tom Win rate:"+player1.winRate());
        System.out.println("jack Win rate:"+player2.winRate());
    }
    public static void hhh2(){
        Random random = new Random();
        for (int a=0;a<100;a++){
            System.out.println(random.nextInt(5));
        }
    }
}
```
