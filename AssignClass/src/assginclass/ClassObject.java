package assginclass;

import java.util.ArrayList;
import java.util.List;

/**
 * @author ice
 * @date 19-6-12
 */
public class ClassObject implements Comparable<ClassObject>{

    private List<Student> students = new ArrayList<>();

    private List<Integer> combine = new ArrayList<>();

    public List<Integer> getCombine() {
        return combine;
    }

    public void setCombine(List<Integer> combine) {
        this.combine = combine;
    }

    public int length() {
        return students.size();
    }

    public List<Student> getStudents() {
        return students;
    }

    public void setStudents(List<Student> students) {
        this.students = students;
    }

    static List<Integer> getDoubleMaxCombine(List<Student> students) {
        int[][] weight = new int[6][6];
        // 统计选科组合人数
        for (Student student : students) {
            List<Integer> subjects = student.getSubjects();
            int length = subjects.size();
            for (int i = 0; i < length - 1; i++) {
                for (int j = i + 1; j < length; j++) {
                    weight[subjects.get(i)][subjects.get(j)] += 1;
                }
            }
        }
        // 求最大选科组合
        int max1 = 0, max2 = 0;
        int maxCount = 0;
        for (int i = 0; i < weight.length; i++) {
            for (int j = i; j < weight.length; j++) {
                int count = weight[i][j] + weight[j][i];
                if (count > maxCount) {
                    max1 = i;
                    max2 = j;
                    maxCount = count;
                }
            }
        }
        List<Integer> combine = new ArrayList<>();
        combine.add(max2);
        combine.add(max1);
        return combine;
    }

    public static List<Student> getRemoveStudents(List<Student> students, int combineLength) {
        List<Integer> combine = ClassObject.getMaxCombine(students, combineLength);
        List<Student> removeStudents = new ArrayList<>();
        for (int i = students.size() - 1; i >= 0; i--) {
            Student student = students.get(i);
            List<Integer> subjects = student.getSubjects();
            int count = 0;
            for (int subject : subjects) {
                for (int subjectInCombine : combine) {
                    if (subjectInCombine == subject) {
                        count += 1;
                    }
                }
            }
            if (count < combineLength) {
                students.remove(i);
                removeStudents.add(student);
            }
        }
        return removeStudents;
    }

    static List<Integer> getSingleMax(List<Student> students) {
        int[] weight = new int[6];
        for (Student student : students) {
            List<Integer> subjects = student.getSubjects();
            int length = subjects.size();
            for (int i = 0; i < length; i++) {
                int subject = subjects.get(i);
                weight[subject] += 1;
            }
        }
        // 选出最大的组合
        int max_subject = 0;
        for (int i = 0; i < weight.length; i++) {
            if (weight[i] > weight[max_subject]) {
                max_subject = i;
            }
        }
        List<Integer> combine = new ArrayList<>();
        combine.add(max_subject);
        return combine;
    }
    public static List<Integer> getMaxCombine(List<Student> students, int combineLength) {
        if (combineLength == 2) {
            return getDoubleMaxCombine(students);
        }
        if (combineLength == 1) {
            return getSingleMax(students);
        }
        throw new RuntimeException("combineLength should be not null");
    }
    @Override
    public int compareTo(ClassObject o) {
        return students.size() - o.getStudents().size();
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(students.size()).append("  ");
        for (int subject: combine) {
            sb.append(subject + ",");
        }
        return sb.toString();
    }
}
