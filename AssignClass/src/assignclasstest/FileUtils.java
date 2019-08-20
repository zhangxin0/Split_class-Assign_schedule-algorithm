package assignclasstest;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

/**
 * @author ice
 * @date 19-6-4
 */
public class FileUtils {

    private static final String CSV_SEPARATOR = ",";

    public static List<String[]> readCsv(String path) throws Exception{
        File dataFile = new File(path);
        BufferedReader br = new BufferedReader(new FileReader(dataFile));
        String line;
        String data;
        List<String[]> content = new ArrayList<>();
        while((line = br.readLine()) != null) {
            data = line;
            String[] strings = data.split(CSV_SEPARATOR);
            content.add(strings);
        }
        return content;
    }
}
