package assignclasstest;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * @author ice
 * @date 19-6-11
 */
public class GenerateSubjects {

    /**
     * 学生人数
     */
    public static final int STUDENT_NUM = 300;

    /**
     * 科目
     */
    private static Integer[] subjects = {1, 2, 3, 4, 5, 6};

    /**
     * 权重
     */
    private static int[] weight = {3, 3, 3, 1, 1, 2};

    public static List generate() {
        List<float[]> data = new ArrayList<>();
        Random random = new Random();
        // 在subject_list 中添加权重个数的
        List<Integer> subject_list = new ArrayList<>();
        for (int i = 0; i < weight.length; i++) {
            for (int j = 0; j < weight[i]; j++) {
                subject_list.add(subjects[i]);
            }
        }
        int count = 0;
        while (data.size() < STUDENT_NUM) {
            float[] floats = {0, 0, 0, 0, 0, 0, 0};
            List<Integer> subject_list_copy = new ArrayList<Integer>();
            for (Integer item : subject_list) {
                subject_list_copy.add(item);
            }
            for (int i = 0; i < 3; i++) {
                int index = random.nextInt(subject_list_copy.size());
                int value = subject_list_copy.get(index);
                floats[value - 1] = 1;
                for (int j = subject_list_copy.size() - 1; j >=0; j--) {
                    if (subject_list_copy.get(j) == value) {
                        subject_list_copy.remove(j);
                    }
                }
            }
            floats[floats.length - 1] = count;
            data.add(floats);
            count += 1;
        }

        return data;
    }

    public static void main(String[] args) {
        GenerateSubjects.generate();
    }
}
