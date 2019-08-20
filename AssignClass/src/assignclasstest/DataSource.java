package assignclasstest;
import java.util.ArrayList;
import java.util.List;

/**
 * @author ice
 * @date 19-6-4
 * @date 19-6-5
 */
public class DataSource {

    public static ArrayList<float[]> getStudentSubject() {
        String path = System.getProperty("user.dir") + "/src/data/subjects2.txt";
        try {
            List<String[]> data = FileUtils.readCsv(path);
            ArrayList<float[]> result = new ArrayList<>();
            int index = 0;
            for (String[] strings : data) {
                if (strings.length <= 0) {
                    continue;
                }
                String subjects = strings[0];
                float[] floats = new float[subjects.length() + 1];
                for (int i = 0; i < subjects.length(); i++) {
                    float value = Float.parseFloat(subjects.charAt(i) + "");
                    floats[i] = value;
                }
                floats[subjects.length()] = index;
                result.add(floats);
                index += 1;
            }
            return result;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
    public static void main(String[] args) {
        System.out.println(DataSource.getStudentSubject());
    }
}
