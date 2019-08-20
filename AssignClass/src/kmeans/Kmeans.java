package kmeans;

import java.util.ArrayList;
import java.util.Random;

/**
 * K均值聚类算法
 */
public class Kmeans {

    /**
     * 分成多少簇
     */
    private int numOfCluster;
    /**
     * 迭代次数
     */
    private int timeOfIteration;
    /**
     * 数据集元素个数，即数据集的长度
     */
    private int dataSetLength;
    private ArrayList<float[]> dataSet;
    /**
     * 中心链表
     */
    private ArrayList<float[]> center;
    /**
     * 簇
     */
    private ArrayList<ArrayList<float[]>> cluster;
    /**
     * 误差平方和
     */
    private ArrayList<Float> sumOfErrorSquare;
    private Random random;

    public static final int DEFAULT_NUM_OF_CLUSTER = 6;

    /**
     * float[] 数组的用于计算距离的长度，
     */
    private int calculationLength = 6;
    /**
     * 设置需分组的原始数据集
     *
     * @param dataSet
     */

    public void setDataSet(ArrayList<float[]> dataSet) {
        this.dataSet = dataSet;
    }

    /**
     * 获取结果分组
     *
     * @return 结果集
     */

    public ArrayList<ArrayList<float[]>> getCluster() {
        return cluster;
    }

    /**
     * 构造函数，传入需要分成的簇数量
     *
     * @param numOfCluster 簇数量,若numOfCluster<=0时，设置为1，若numOfCluster大于数据源的长度时，置为数据源的长度
     */
    public Kmeans(int numOfCluster) {
        if (numOfCluster <= 0) {
            numOfCluster = DEFAULT_NUM_OF_CLUSTER;
        }
        this.numOfCluster = numOfCluster;
    }

    /**
     * 初始化
     */
    private void init() {
        timeOfIteration = 0;
        random = new Random();
        //如果调用者未初始化数据集，则采用内部测试数据集
        if (dataSet == null || dataSet.size() == 0) {
            throw new RuntimeException("数据集不能为空");
        }
        dataSetLength = dataSet.size();
        //若numOfCluster大于数据源的长度时，置为数据源的长度
        if (numOfCluster > dataSetLength) {
            numOfCluster = dataSetLength;
        }
        center = initCenters();
        cluster = initCluster();
        sumOfErrorSquare = new ArrayList<>();
    }

    /**
     * 初始化中心数据链表，分成多少簇就有多少个中心点
     *
     * @return 中心点集
     */
    private ArrayList<float[]> initCenters() {
        ArrayList<float[]> center = new ArrayList<>();
        int[] randoms = new int[numOfCluster];
        boolean flag;
        int temp = random.nextInt(dataSetLength);
        randoms[0] = temp;
        //randoms数组中存放数据集的不同的下标
        for (int i = 1; i < numOfCluster; i++) {
            flag = true;
            while (flag) {
                temp = random.nextInt(dataSetLength);
                int j = 0;
                for (j = 0; j < i; j++) {
                    if (randoms[j] == temp) {
                        break;
                    }
                }

                if (j == i) {
                    flag = false;
                }
            }
            randoms[i] = temp;
        }
        // 测试随机数生成情况
//        for (int i = 0; i < numOfCluster; i++) {
//            System.out.println("test1:randoms[" + i + "]=" + randoms[i] + ":" + dataSet.get(randoms[i])[0] + "," + dataSet.get(randoms[i])[1] + "," + dataSet.get(randoms[i])[2] + "," + dataSet.get(randoms[i])[3] + "," + dataSet.get(randoms[i])[4] + "," + dataSet.get(randoms[i])[5]);
//        }
//        System.out.println();
        for (int i = 0; i < numOfCluster; i++) {
            // 生成初始化中心链表
            center.add(dataSet.get(randoms[i]));
        }
        return center;
    }

    /**
     * 初始化簇集合
     *
     * @return 一个分为k簇的空数据的簇集合
     */
    private ArrayList<ArrayList<float[]>> initCluster() {
        ArrayList<ArrayList<float[]>> cluster = new ArrayList<>();
        for (int i = 0; i < numOfCluster; i++) {
            cluster.add(new ArrayList<>());
        }
        return cluster;
    }

    /**
     * 计算两个点之间的距离
     *
     * @param element 点1
     * @param center  点2
     * @return 距离
     */
    private float distance(float[] element, float[] center) {
        float distance;
        float r = 0;
        for (int i = 0; i < calculationLength; i++) {
            r += (element[i] - center[i]) * (element[i] - center[i]);
        }
        distance = (float) Math.sqrt(r);
        return distance;
    }

    /**
     * 获取距离集合中最小距离的位置
     *
     * @param distance 距离数组
     * @return 最小距离在距离数组中的位置
     * 加入班级人数限制
     */
    private int minDistance(float[] distance) {
        float minDistance = Float.MAX_VALUE;
        int minLocation = 0;
        for (int i = 0; i < distance.length; i++) {
            if (distance[i] <= minDistance) {
                minDistance = distance[i];
                minLocation = i;
            }
        }
        return minLocation;
    }

    /**
     * 核心，将当前元素放到最小距离中心相关的簇中
     */
    private void clusterSet() {
        float[] distance = new float[numOfCluster];
        for (int i = 0; i < dataSetLength; i++) {
            for (int j = 0; j < numOfCluster; j++) {
                // 计算每个点对聚类中心的距离，选取最小的
                distance[j] = distance(dataSet.get(i), center.get(j));
            }
            // 计算当前个体聚类最近的聚类中心 minLocation, 然后将当前个体加入聚类中心中
            int minLocation = minDistance(distance);

            // 核心，将当前元素放到最小距离中心相关的簇中
            cluster.get(minLocation).add(dataSet.get(i));

        }
    }

    /**
     * 求两点误差平方的方法
     *
     * @param element 点1
     * @param center  点2
     * @return 误差平方
     */
    private float errorSquare(float[] element, float[] center) {
        float r = 0;
        for (int i = 0; i < calculationLength; i++) {
            r += (element[i] - center[i]) * (element[i] - center[i]);
        }
        return r;
    }

    /**
     * 计算误差平方和准则函数方法
     */
    private void countRule() {
        float jcF = 0;
        for (int i = 0; i < cluster.size(); i++) {
            for (int j = 0; j < cluster.get(i).size(); j++) {
                jcF += errorSquare(cluster.get(i).get(j), center.get(i));
            }
        }
        sumOfErrorSquare.add(jcF);
    }

    /**
     * 设置新的簇中心方法
     */
    private void setNewCenter() {
        for (int i = 0; i < numOfCluster; i++) {
            int n = cluster.get(i).size();
            if (n != 0) {
                float[] newCenter = new float[calculationLength];
                for (int j = 0; j < n; j++) {
                    for (int k = 0; k < calculationLength; k++) {
                        newCenter[k] += cluster.get(i).get(j)[k];
                    }
//                    newCenter[0] += cluster.get(i).get(j)[0];
//                    newCenter[1] += cluster.get(i).get(j)[1];
//                    newCenter[2] += cluster.get(i).get(j)[2];
//                    newCenter[3] += cluster.get(i).get(j)[3];
//                    newCenter[4] += cluster.get(i).get(j)[4];
//                    newCenter[5] += cluster.get(i).get(j)[5];
                }

                for (int k = 0; k < calculationLength; k++) {
                    newCenter[k] = newCenter[k] / n;
                }
                // 设置一个平均值
//                newCenter[0] = newCenter[0] / n;
//                newCenter[1] = newCenter[1] / n;
//                newCenter[2] = newCenter[2] / n;
//                newCenter[3] = newCenter[3] / n;
//                newCenter[4] = newCenter[4] / n;
//                newCenter[5] = newCenter[5] / n;
                center.set(i, newCenter);
            }
        }
    }

    /**
     * 打印数据，测试用
     *
     * @param dataArray     数据集
     * @param dataArrayName 数据集名称
     */
    public void printDataArray(ArrayList<float[]> dataArray,
                               String dataArrayName) {
        for (int i = 0; i < dataArray.size(); i++) {
            System.out.println("print:" + dataArrayName + "[" + i + "]={"
                    + dataArray.get(i)[0] + "," + dataArray.get(i)[1] + "," + dataArray.get(i)[2] + "," + dataArray.get(i)[3] + "," + dataArray.get(i)[4] + "," + dataArray.get(i)[5] + "}");
        }
        System.out.println("===================================");
    }

    /**
     * Kmeans算法核心过程方法
     */
    private void kmeans() {
        init();
        // 循环分组，直到误差不变为止
        while (true) {
            clusterSet();

            countRule();

            // 误差不变了，分组完成
            if (timeOfIteration != 0) {
                if (sumOfErrorSquare.get(timeOfIteration) - sumOfErrorSquare.get(timeOfIteration - 1) == 0) {
                    break;
                }
            }

            setNewCenter();
            timeOfIteration++;
            cluster.clear();
            cluster = initCluster();
        }
    }

    /**
     * 执行算法
     */
    public void execute() {
        kmeans();
    }

    public int getCalculationLength() {
        return calculationLength;
    }

    public void setCalculationLength(int calculationLength) {
        this.calculationLength = calculationLength;
    }
}