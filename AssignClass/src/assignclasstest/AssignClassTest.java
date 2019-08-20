package assignclasstest;

import assginclass.AssignClass;
import assginclass.Student;
import kmeans.Kmeans;

import java.util.ArrayList;
import java.util.List;

/**
 * @author ice
 * @date 19-6-13
 */
public class AssignClassTest {

    public static void main(String[] args) {
        List<float[]> data = DataSource.getStudentSubject();

        List<Student> students = AssignClassTest.getStudents(data);
        AssignClass assignClass = new AssignClass();

        assignClass.setStudents(students);
        assignClass.init();
        assignClass.run();
    }

    public static List<Student> getStudents(List<float[]> group) {
        List<Student> students = new ArrayList<>();
        for (float[] item : group) {
            List<Integer> subjects = new ArrayList<>();
            for (int i = 0; i < Kmeans.DEFAULT_NUM_OF_CLUSTER; i++) {
                if ((int) item[i] == 1) {
                    subjects.add(i);
                }
            }
            Student student = new Student();
            student.setSubjects(subjects);
            student.setCode((int) item[Kmeans.DEFAULT_NUM_OF_CLUSTER]);
            students.add(student);
        }
        return students;
    }
}
