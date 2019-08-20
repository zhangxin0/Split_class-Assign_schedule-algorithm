package assginclass;

import java.util.List;

/**
 * @author ice
 * @date 19-6-12
 */
public class Student {

    private List<Integer> subjects;

    private int code;

    private double score;

    public List<Integer> getSubjects() {
        return subjects;
    }

    public void setSubjects(List<Integer> subjects) {
        this.subjects = subjects;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public double getScore() {
        return score;
    }

    public void setScore(double score) {
        this.score = score;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int subject : subjects) {
            sb.append(subject).append(",");
        }
        return sb.toString() + score;
    }
}
