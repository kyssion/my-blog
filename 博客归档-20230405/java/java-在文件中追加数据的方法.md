```java
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.RandomAccessFile;
 
 
public class JavaAddContent {
	
	/**
	 * 追加使用BufferedWriter
	 * @param fileName
	 * @param content
	 */
	 public static void text1(String fileName, String content) {
		 BufferedWriter out = null;     
	        try {     
	            out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(fileName, true)));     
	            out.write(content);  
	            System.out.println("text1写入~~~");
	        } catch (Exception e) {     
	            e.printStackTrace();     
	        } finally {     
	            try {     
	                if(out != null){  
	                    out.close();     
	                }  
	            } catch (IOException e) {     
	                e.printStackTrace();     
	            }     
	        }     
	 }
	    /**   
	     * 追加文件：使用FileWriter   
	     *    
	     * @param fileName   
	     * @param content   
	     */    
	    public static void text2(String fileName, String content) {   
	        FileWriter writer = null;  
	        try {     
	            // 打开一个写文件器，构造函数中的第二个参数true表示以追加形式写文件     
	            writer = new FileWriter(fileName, true);     
	            writer.write(content); 
	            System.out.println("text2写入~~~");
	        } catch (IOException e) {     
	            e.printStackTrace();     
	        } finally {     
	            try {     
	                if(writer != null){  
	                    writer.close();     
	                }  
	            } catch (IOException e) {     
	                e.printStackTrace();     
	            }     
	        }   
	    }     
	    
	    /**   
	     * 追加文件：使用RandomAccessFile   
	     *    
	     * @param fileName 文件名   
	     * @param content 追加的内容   
	     */    
	    public static void text3(String fileName, String content) {   
	        RandomAccessFile randomFile = null;  
	        try {     
	            // 打开一个随机访问文件流，按读写方式     
	            randomFile = new RandomAccessFile(fileName, "rw");     
	            // 文件长度，字节数     
	            long fileLength = randomFile.length();     
	            // 将写文件指针移到文件尾。     
	            randomFile.seek(fileLength);     
	            randomFile.writeBytes(content);  
	            System.out.println("text3写入~~~");
	        } catch (IOException e) {     
	            e.printStackTrace();     
	        } finally{  
	            if(randomFile != null){  
	                try {  
	                    randomFile.close();  
	                } catch (IOException e) {  
	                    e.printStackTrace();  
	                }  
	            }  
	        }  
	    }   
	    
	    /**
	     * 在文件的前面进行追加
	     * @param fileName
	     * @param content
	     *
	     */
	    public static void text4(String fileName, String content) {
	        BufferedReader reader;
			try {
				reader = new BufferedReader(new FileReader(fileName));
				 String line=null;
			        //一行一行的读取
			        StringBuilder sb=new StringBuilder();
			        sb.append(content);
						while((line=reader.readLine())!=null) {
							sb.append(line);
							sb.append("\r\n");
							 System.out.println( new String(reader.readLine().getBytes("ISO-8859-1"), "UTF-8")); //UTF-8是你文本编码格式
							}
						 reader.close();
				         //写回去
				         RandomAccessFile write=new RandomAccessFile(fileName,"rw");
				       //  write.writeBytes(sb.toString());//会产生中文乱码
				         write(sb.toString().getBytes());
				         System.out.println("text4写入~~");
				         write.close();
			} catch (FileNotFoundException e1) {
				e1.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
	      }
 
	    
	    private static void write(byte[] bytes) {
			// TODO Auto-generated method stub
			
		}
		public static void main(String[] args) {  
	        try{  
	            File file = new File("d://text.txt");  
	            if(file.createNewFile()){  
	                System.out.println("Create file successed");  
	            }
	            text1("d://text.txt", "123"+"\r\n");
	            text2("d://text.txt", "456"+"\r\n");  
	            text3("d://text.txt", "789"+"\r\n"); 
	            text4("d://text.txt", "撒范德萨"+"\r\n");
	        }catch(Exception e){  
	            System.out.println(e);  
	        }  
	    }
}
```