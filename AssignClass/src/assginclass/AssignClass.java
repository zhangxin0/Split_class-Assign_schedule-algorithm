package assginclass;

import kmeans.Kmeans;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * @author ice
 * @date 19-6-12
 */
public class AssignClass {

    private int maxStudentNum = 38;

    private int minStudentNum = 25;

    private int minGoClassStudent = 15;

    private ArrayList<float[]> studentSubjects = new ArrayList<>();

    private List<Student> students = new ArrayList<>();

    private Kmeans kmeans;

    private int numOfCluster = 6;

    private int combineLength = 2;

    private ArrayList<ClassObject> classes;

    public void init() {
        this.studentSubjects = toStudentSubjects(this.students);
        kmeans = new Kmeans(numOfCluster);
        kmeans.setDataSet(studentSubjects);
        kmeans.setCalculationLength(6);

        classes = new ArrayList<>();
    }

    private void reset() {
        classes = new ArrayList<>();
    }

    public void run() {
        int iteration = 1;
        while (true) {
            System.out.println("第" + iteration + "迭代");
            reset();
            // 执行聚类算法获得结果
            runKMeans();
            iteration += 1;

            System.out.println("聚类算法结果");
            removeZero();
            List<Student> removesStudent = removeStudentsAndAssign();

            if (removesStudent.size() > 0) {
                continue;
            }

            removeZero();

            divideClasses();

            reAssign();

            if (isFit() && couldGo()) {
                printClasses();
                break;
            }

        }
    }

    private void printClasses() {
        for (ClassObject classObject : classes) {
            System.out.println(classObject);
        }
    }

    private void verify() {

    }

    private void runKMeans() {
        kmeans.execute();
        ArrayList<ArrayList<float[]>> cluster= kmeans.getCluster();
        for (ArrayList<float[]> group : cluster) {
            ClassObject classObject = new ClassObject();
            classObject.setStudents(getStudents(group));
            classes.add(classObject);
        }
    }

    private List<Student> removeStudentsAndAssign() {
        List<Student> removeStudents = new ArrayList<>();
        for (ClassObject classObject : classes) {
            List<Student> students = ClassObject.getRemoveStudents(classObject.getStudents(), combineLength);
            removeStudents.addAll(students);
            System.out.println(classObject.getStudents().size() + " remove " + students.size());
        }
        // 重新分配学生
        for (ClassObject classObject : classes) {
            classObject.setCombine(ClassObject.getMaxCombine(classObject.getStudents(), combineLength));
        }

        for (int i = removeStudents.size() - 1; i >= 0; i--) {
            Student student = removeStudents.get(i);
            List<Integer> subjects = student.getSubjects();
            for (ClassObject classObject : classes) {
                List<Integer> combine = classObject.getCombine();
                int count = 0;
                for (int subject : subjects) {
                    for (int combineSubject : combine) {
                        if (subject == combineSubject) {
                            count += 1;
                        }
                    }
                }
                if (count >= combineLength) {
                    classObject.getStudents().add(student);
                    removeStudents.remove(i);
                    break;
                }
            }
        }
        return removeStudents;
    }

    private boolean couldGo() {
        boolean couldGoFlag = true;
        int[] total = new int[Kmeans.DEFAULT_NUM_OF_CLUSTER];
        for (ClassObject classObject : classes) {
            List<Student> students = classObject.getStudents();
            List<Integer> combine = classObject.getCombine();
            for (Student student : students) {
                List<Integer> subjects = student.getSubjects();

                for (Integer subject : subjects) {
                    boolean exist = false;
                    for (Integer combine_subject : combine) {
                        if (subject.equals(combine_subject)) {
                            exist = true;
                            break;
                        }
                    }
                    if (!exist) {
                        total[subject] += 1;
                    }
                }
            }
        }

        int class_count = 0;
        for (int i = 0; i < total.length; i++) {

            if (total[i] < minGoClassStudent) {
                couldGoFlag = false;
                return false;
            }

            if (total[i] < 25) {
                class_count += 1;
                continue;
            }
            int left = total[i] / maxStudentNum;
            int remain = total[i] % maxStudentNum;
            if (remain == 0) {
                class_count += left;
            } else {
                class_count = class_count + left + 1;
            }
        }
        System.out.println("can assign class num:" + class_count);
        for (int i = 0; i < total.length; i++) {
            System.out.println("class of subject " + i + " : " + total[i]);
        }
        return couldGoFlag;
    }

    private void removeZero() {
        for (int i = classes.size() - 1; i >= 0; i--) {
            ClassObject classObject = classes.get(i);
            List<Student> students = classObject.getStudents();
            if (students == null || students.size() == 0) {
                classes.remove(i);
            }
        }
    }

    private void divideClasses() {
        for (int i = classes.size() - 1; i >= 0; i--) {
            ClassObject classObject = classes.get(i);
            List<Student> students = classObject.getStudents();
            int studentNum = students.size();
            if (studentNum < maxStudentNum) {
                continue;
            }
            int left = (int) Math.ceil((double) studentNum / maxStudentNum);
            int right = (int) Math.floor((double) studentNum / minStudentNum);

            if (left <= right) {
                int step = maxStudentNum;

                int studentLength = students.size();
                int start = 0, end = 0;
                List<List<Student>> newClassList = new ArrayList<>();
                while (start < studentLength) {
                    end = start + step;
                    if (end >= studentLength) {
                        end = studentLength;
                    }

                    List<Student> partStudents = cutStudentList(students, start, end);
                    ClassObject classObject1 = new ClassObject();
                    classObject1.setStudents(partStudents);
                    classObject1.setCombine(classObject.getCombine());

                    classes.add(classObject1);

                    newClassList.add(partStudents);

                    start = end;
                }

                fix(newClassList);
                classes.remove(i);
            }
        }
    }

    private void fix(List<List<Student>> classList) {
        for (List<Student> students : classList) {
            int studentNum = students.size();
            if (studentNum < minStudentNum) {
                int needStudentNum = minStudentNum - studentNum;
                List<Student> needStudent = new ArrayList<>();
                for (List<Student> students1 : classList) {
                    while (students1.size() > minStudentNum
                            && needStudent.size() < needStudentNum) {
                        int last = students1.size() - 1;
                        needStudent.add(students1.get(last));
                        students1.remove(last);
                    }
                }
                students.addAll(needStudent);
            }
        }
    }

    private List<Student> cutStudentList(List<Student> students, int start , int end) {
        List<Student> newStudents = new ArrayList<>();
        for (int i = start; i < end; i++) {
            newStudents.add(students.get(i));
        }
        return newStudents;
    }

    /**
     * 人数少的增，人数多的减
     */
    private void reAssign() {
        List<ClassObject> needFixClass = new ArrayList<>();
        for (ClassObject classObject : classes) {
            List<Student> students = classObject.getStudents();
            int studentNum = students.size();
            if (studentNum < minStudentNum || studentNum > maxStudentNum) {
                needFixClass.add(classObject);
            }
        }

        for (ClassObject classObject : needFixClass) {
            int studentNum = classObject.getStudents().size();
            if (studentNum <= maxStudentNum && studentNum >= minStudentNum) {
                continue;
            } else if (studentNum < minStudentNum) {
                lessMin(classObject);
            } else if (studentNum > maxStudentNum) {
                greatMax(classObject);
            }

        }
    }

    private void greatMax(ClassObject classObject) {
        int studentNum = classObject.getStudents().size();
        int removeStudentNum = studentNum - maxStudentNum;

        List<Student> students = classObject.getStudents();

        int count = 0;
        for (int i = students.size() - 1; i >= 0 && count < removeStudentNum; i--) {
            Student student = students.get(i);
            for (ClassObject classObject1 : classes) {
                if (classObject1.getStudents().size() < maxStudentNum
                        && inCombine(student, classObject1.getCombine())) {
                    classObject1.getStudents().add(student);
                    students.remove(i);
                    count += 1;
                    break;
                }
            }
        }
    }

    private void lessMin(ClassObject classObject) {
        int studentNum = classObject.getStudents().size();
        int needStudentNum = minStudentNum - studentNum;
        List<Student> needStudents = new ArrayList<>();
        Collections.sort(classes);
        for (int i = classes.size() - 1; i >= 0; i--) {
            ClassObject otherClass = classes.get(i);
            List<Student> otherStudents = otherClass.getStudents();
            int otherStudentNum = otherStudents.size();

            if (needStudents.size() == needStudentNum) {
                break;
            }

            if (otherClass != classObject && otherStudentNum > minStudentNum) {
                for (int j = otherStudents.size() - 1; j >= 0; j--) {
                    Student student = otherStudents.get(i);
                    if (inCombine(student, classObject.getCombine())) {
                        needStudents.add(student);
                        otherStudents.remove(j);
                        if (needStudents.size() == needStudentNum) {
                            break;
                        }
                    }
                }
            }
        }

        classObject.getStudents().addAll(needStudents);
    }

    private boolean inCombine(Student student, List<Integer> combine) {
        List<Integer> subjects = student.getSubjects();
        int count = 0;
        for (int subject : subjects) {
            for (int combineSubject : combine) {
                if (subject == combineSubject) {
                    count += 1;
                }
            }
        }
        if (count >= combineLength) {
            return true;
        }
        return false;
    }

    private boolean isFit() {
        for (ClassObject classObject : classes) {
            int studentNum = classObject.getStudents().size();
            if (studentNum < minStudentNum || studentNum > maxStudentNum) {
                return false;
            }
        }
        return true;
    }

    /**
     * 转换学生信息
     * @param group
     * @return
     */
    private List<Student> getStudents(ArrayList<float[]> group) {
        List<Student> students = new ArrayList<>();
        for (float[] item : group) {
            students.add(this.students.get((int) item[Kmeans.DEFAULT_NUM_OF_CLUSTER]));
        }
        return students;
    }

    public List<Student> getStudents() {
        return students;
    }

    public void setStudents(List<Student> students) {
        this.students = students;
    }

    private ArrayList<float[]> toStudentSubjects(List<Student> students) {
        ArrayList<float[]> studentSubjects = new ArrayList<>();
        for (int i = 0; i < students.size(); i++) {
            // 转换格式
            Student student = students.get(i);
            List<Integer> subjects = student.getSubjects();
            float[] studentSubject = new float[Kmeans.DEFAULT_NUM_OF_CLUSTER + 1];
            for (Integer subject : subjects) {
                studentSubject[subject] = 1;
            }
            studentSubject[studentSubject.length - 1] = i;
            studentSubjects.add(studentSubject);
        }
        return studentSubjects;
    }
}
