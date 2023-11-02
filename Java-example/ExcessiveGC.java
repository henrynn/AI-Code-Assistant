/**

Excessive garbage allocation may happen when the program creates a lot of short-lived objects. The garbage collector works continuously, removing unneeded objects from memory, which impacts applications’ performance in a negative way

**/

public class ExcessiveGC{
	
	public void addString(){
		String oneMillionHello = "";
		for (int i = 0; i < 1000000; i++) {
			oneMillionHello = oneMillionHello + "Hello!";
		}
		System.out.println(oneMillionHello.substring(0, 6));
	}
	
	public static void main(String[] args){
		ExcessiveGC exc = new ExcessiveGC();
		exc.addString();
	}
}