# kafka consumer

# kafka 消费者与消费组

消费者（Consumer）负责订阅Kafka中的主题（Topic），并且从订阅的主题上拉取消息。与其他一些消息中间件不同的是：在Kafka的消费理念中还有一层消费组（Consumer Group）的概念，每个消费者都有一个对应的消费组。当消息发布到主题后，只会被投递给订阅它的每个消费组中的一个消费者

kafka这块的模型大致是这种结构：

主题 - 细分成分区 -> 消费者组订阅主题 -> 组中的消费者分别订阅 分区

对于消息中间件而言，一般有两种消息投递模式：点对点（P2P，Point-to-Point）模式和发布/订阅（Pub/Sub）模式。
- 点对点模式是基于队列的，消息生产者发送消息到队列，消息消费者从队列中接收消息。
- 发布订阅模式定义了如何向一个内容节点发布和订阅消息，这个内容节点称为主题（Topic），主题可以认为是消息传递的中介，消息发布者将消息发布到某个主题，而消息订阅者从主题中订阅消息。

消费者并非逻辑上的概念，它是实际的应用实例，它可以是一个线程，也可以是一个进程。同一个消费组内的消费者既可以部署在同一台机器上，也可以部署在不同的机器上。

每一个消费组都会有一个固定的名称，消费者在进行消费前需要指定其所属消费组的名称，这个可以通过消费者客户端参数group.id来配置，默认值为空字符串。

主题使得消息的订阅者和发布者互相保持独立，不需要进行接触即可保证消息的传递，发布/订阅模式在消息的一对多广播时采用。Kafka 同时支持两种消息投递模式，而这正是得益于消费者与消费组模型的契合：

- 如果所有的消费者都隶属于同一个消费组，那么所有的消息都会被均衡地投递给每一个消费者，即每条消息只会被一个消费者处理，这就相当于点对点模式的应用。
- 如果所有的消费者都隶属于不同的消费组，那么所有的消息都会被广播给所有的消费者，即每条消息会被所有的消费者处理，这就相当于发布/订阅模式的应用。

# 一个正常的消费逻辑需要具备以下几个步骤

（1）配置消费者客户端参数及创建相应的消费者实例。
（2）订阅主题。
（3）拉取消息并消费。
（4）提交消费位移。
（5）关闭消费者实例。

针对之前的模型 ， 我们在初始化kafka对应的配置的时候就需要配置这个消费者对应的消费组（和其他订阅者组相同或者不同能决定这个消息是广播还是点对点）


# kafka三种不同订阅状态

集合订阅的方式subscribe（Collection）正则表达式订阅的方式subscribe（Pattern）指定分区的订阅方式assign（Collection）分表代表了三种不同的订阅状态：AUTO_TOPICS、AUTO_PATTERN和USER_ASSIGNED（如果没有订阅，那么订阅状态为NONE）。

USER_ASSIGNED（如果没有订阅，那么订阅状态为NONE）。然而这三种状态是互斥的，在一个消费者中只能使用其中的一种，否则会报出IllegalStateException异常

通过 subscribe（）方法订阅主题具有消费者自动再均衡的功能，在多个消费者的情况下可以根据分区分配策略来自动分配各个消费者与分区的关系。当消费组内的消费者增加或减少时，分区分配关系会自动调整，以实现消费负载均衡及故障自动转移。而通过assign（）方法订阅分区时，是不具备消费者自动均衡的功能的，其实这一点从assign（）方法的参数中就可以看出端倪，两种类型的subscribe（）都有ConsumerRebalanceListener类型参数的方法，而assign（）方法却没有

集合和正则对应：KafkaConsumer.subscribe（）方法
分区订阅对应：KafkaConsumer.assgin（）方法  ， 这个需要制定这个集合定于那个消息的那个位置

# kafka客户端反序列化

同生产者 ， 要一一对应

# kafka 消息消费

Kafka中的消费是基于拉模式的。消息的消费一般有两种模式：推模式和拉模式。推模式是服务端主动将消息推送给消费者，而拉模式是消费者主动向服务端发起请求来拉取消息。

Kafka中的消息消费是一个不断轮询的过程，消费者所要做的就是重复地调用poll（）方法，而poll（）方法返回的是所订阅的主题（分区）上的一组消息

# kafka poll过程

到目前为止，可以简单地认为poll（）方法只是拉取一下消息而已，但就其内部逻辑而言并不简单，它涉及消费位移、消费者协调器、组协调器、消费者的选举、分区分配的分发、再均衡的逻辑、心跳等内容 下面一个一个介绍

## 消费位移

对offset做了一些区分：对于消息在分区中的位置，我们将offset称为“偏移量”；对于消费者消费到的位置，将 offset 称为“位移”，有时候也会更明确地称之为“消费位移”

在每次调用poll（）方法时，它返回的是还没有被消费过的消息集（当然这个前提是消息已经存储在Kafka 中了，并且暂不考虑异常情况的发生），要做到这一点，就需要记录上一次消费时的消费位移。并且这个消费位移必须做持久化保存，而不是单单保存在内存中，否则消费者重启之后就无法知晓之前的消费位移。

在旧消费者客户端中，消费位移是存储在ZooKeeper中的。而在新消费者客户端中，消费位移存储在Kafka内部的主题__consumer_offsets中。这里把将消费位移存储起来（持久化）的动作称为“提交”，消费者在消费完消息之后需要执行消费位移的提交。

因为kafka的订阅机制，在一个主题下的一个分区只能被订阅这个主题的任意消费者组中的一个消费者消费

和之前的HW和LEO 类似 ， 这里提交的偏移量并不是当前消费玩的位置，而是下一个位置

- 在 Kafka 中默认的消费位移的提交方式是自动提交，这个是定期的，消费者每隔5秒会将拉取到的每个分区中最大的消息位移进行提交。自动位移提交的动作是在poll（）方法的逻辑里完成的，在每次真正向服务端发起拉取请求之前会检查是否可以进行位移提交，如果可以，那么就会提交上一次轮询的位移

> 消息异常的两种情况 1. 重复消费：消费完但是结果并没有提交，重新poll导致重新消费 2. 丢失：消费中出现异常，然后poll了，导致异常之后的消息没有被消费

自动位移提交的方式在正常情况下不会发生消息丢失或重复消费的现象，但是在编程的世界里异常无可避免，与此同时，自动位移提交也无法做到精确的位移管理。在Kafka中还提供了手动位移提交的方式，这样可以使得开发人员对消费位移的管理控制更加灵活。应于 KafkaConsumer 中的 commitSync（）和commitAsync（）两种类型的方法。

> kafka手动控制提交commitSync（）

于采用 commitSync（）的无参方法而言，它提交消费位移的频率和拉取批次消息、处理批次消息的频率是一样的，如果想寻求更细粒度的、更精准的提交，那么就需要使用commitSync（）的另一个含参方法

这个手动参数有两个值 ， 一个描述分片的位置 ， 一个描述偏移量

我们在使用的时候可以使用消息类ConsumerRecord的api ， 比如 ConsumerRecords 类的 partitions（）方法和records（TopicPartition）方法获取某个分片中的所有值，或者直接使用offset方法来获取偏移量，topic和patition方法获取主题和分区

> 注意一个点 , kafka这个偏移值在客户端有一份，在服务端也有一份的，客户端如果没有重启的化是以客户端为依据的，如果有重启将会以服务端为依据

## kafka consumer 控制和关闭

KafkaConsumer中使用pause（）和resume（）方法来分别实现暂停某些分区在拉取操作时返回数据给客户端和恢复某些分区向客户端返回数据的操作

```java
void pause(Collection<TopicPartition> partitions);
void resume(Collection<TopicPartition> partitions);
```

KafkaConsumer还提供了一个无参的paused（）方法来返回被暂停的分区集合，此方法的具体定义如下：

```java
Set<TopicPartition> paused();
```

KafkaConsumer的wakeup（）方法，wakeup（）方法是 KafkaConsumer 中唯一可以从其他线程里安全调用的方法（KafkaConsumer 是非线程安全的，可以通过3.2.10节了解更多细节），调用wakeup（）方法后可以退出poll（）的逻辑，并抛出 WakeupException 的异常，我们也不需要处理WakeupException 的异常，它只是一种跳出循环的方式

跳出循环以后一定要显式地执行关闭动作以释放运行过程中占用的各种系统资源，包括内存资源、Socket连接等。KafkaConsumer提供了close（）方法来实现关闭，close（）方法有三种重载方法，分别如下

```java
//todo
```

第二种方法是通过 timeout 参数来设定关闭方法的最长执行时间，有些内部的关闭逻辑会耗费一定的时间，比如设置了自动提交消费位移，这里还会做一次位移提交的动作；而第一种方法没有 timeout 参数，这并不意味着会无限制地等待，它内部设定了最长等待时间（30秒）；第三种方法已被标记为@Deprecated，可以不考虑。

## kafka  指定位移消费

消费位移的提交，正是有了消费位移的持久化，才使消费者在关闭、崩溃或者在遇到再均衡的时候，可以让接替的消费者能够根据存储的消费位移继续进行消费

想一下，当一个新的消费组建立的时候，它根本没有可以查找的消费位移。或者消费组内的一个新消费者订阅了一个新的主题，它也没有可以查找的消费位移。当__consumer_offsets主题中有关这个消费组的位移信息过期而被删除后，它也没有可以查找的消费位移。

在 Kafka 中每当消费者查找不到所记录的消费位移时，就会根据消费者客户端参数auto.offset.reset的配置来决定从何处开始进行消费，这个参数的默认值为“latest”，表示从分区末尾开始消费消息。参考图3-9，按照默认的配置，消费者会从9开始进行消费（9是下一条要写入消息的位置），更加确切地说是从9开始拉取消息。如果将auto.offset.reset参数配置为“earliest”，那么消费者会从起始处，也就是0开始消费。

auto.offset.reset参数还有一个可配置的值—“none”，配置为此值就意味着出现查到不到消费位移的时候，既不从最新的消息位置处开始消费，也不从最早的消息位置处开始消费，此时会报出NoOffsetForPartitionException异常

到目前为止，我们知道消息的拉取是根据poll（）方法中的逻辑来处理的，这个poll（）方法中的逻辑对于普通的开发人员而言是一个黑盒，无法精确地掌控其消费的起始位置。提供的auto.offset.reset 参数也只能在找不到消费位移或位移越界的情况下粗粒度地从开头或末尾开始消费。有些时候，我们需要一种更细粒度的掌控，可以让我们从特定的位移处开始拉取消息，而 KafkaConsumer 中的 seek（）方法正好提供了这个功能，让我们得以追前消费或回溯消费。seek（）方法的具体定义如下

```java
void seek(TopicPartition partition, long offset);
```

seek（）方法中的参数partition表示分区，而offset参数用来指定从分区的哪个位置开始消费。seek（）方法只能重置消费者分配到的分区的消费位置，而分区的分配是在 poll（）方法的调用过程中实现的。也就是说，在执行seek（）方法之前需要先执行一次poll（）方法，等到分配到分区之后才可以重置消费位置。

//剩下的如何设置略 > 暂时没有遇到场景


## kafka再均衡

