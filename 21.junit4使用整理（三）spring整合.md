> 这里记录一下spring 和 junit4进行整合例子

现在情况下spring支持的junit版本不是很高 使用junit4.1.2进行开发

```java
import javax.annotation.Resource;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.BeansException;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.transaction.annotation.Transactional;
import b_spring.a_spring的bean的依赖注入.bean.DemoBeanOne;
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations ={"classpath:a_bean.xml"})
@Transactional
public class TestForOneMain implements ApplicationContextAware{
	ApplicationContext context;
	@Resource(name="demoOne")
	DemoBeanOne demoBeanOne;
	@Test
	@Transactional//指定可以进行事物
	@Rollback(value=true)//声明事物操作
	public void test() {
		
	}
	@Override
	public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
		// TODO Auto-generated method stub
		this.context=applicationContext;
	}
}
```

- @RunWith：用于指定junit运行环境，是junit提供给其他框架测试环境接口扩展，为了便于使用spring的依赖注入，spring提供了org.springframework.test.context.junit4.SpringJUnit4ClassRunner作为Junit测试环境
- @ContextConfiguration({“classpath:applicationContext.xml”,”classpath:spring/buyer/applicationContext-service.xml”}) 导入配置文件，这里我的applicationContext配置文件是根据模块来分类的。如果有多个模块就引入多个“applicationContext-service.xml”文件。如果所有的都是写在“applicationContext。xml”中则这样导入