
/**
Excessive usage of static fields can potentially lead to a memory leak. In Java, static fields usually remain in memory as long as the application is running
**/

public class StaticFieldsMemoryLeakExample {
    private static List<Integer> integers = new ArrayList<Integer>();

    public void insertIntegers() {
        for (int i = 0; i < 100000000; i++) {
            integers.add(i);
        }
    }

    public static void main(String[] args) {
        new StaticFieldsMemoryLeakExample().insertIntegers();
    }
}