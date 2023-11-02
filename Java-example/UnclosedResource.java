
/**

Resources such as connections and streams utilize memory. If they are not closed, memory allocated to these resources is blocked and the GC is unable to free up this space

**/

public cloass UnclosedResource{
	
public void readFromURL() {
    try {
        URL url = new URL("http://example.com");
        URLConnection urlConnection = url.openConnection();
        InputStream is = urlConnection.getInputStream();
        byte[] bytes = is.readAllBytes();
    } catch (IOException ioe) {
        ioe.printStackTrace();
    }
}

public static void main(String[] args){
	UnclosedResource resource = new UnclosedResource();
	resource.readFromURL();
}

}