class GC38 {
    private static final int _1MB = 1024 * 1024;

    public static void main(String[] args) {
        byte[] allocation;
        //直接分配在老年代
        allocation = new byte[4 *  _1MB];
    }
}