public class ExponentialSchedule implements AnnealingSchedule {

    private int iterations;
    private double temperature = 10000;
    private double rate;

    public ExponentialSchedule(int size, double rate) {
        this.iterations = size;
        this.rate = rate;
    }

    @Override
    public boolean hasNext() {
        return rate * temperature >= 0.0001;
    }

    @Override
    public double nextTemperature() {
        temperature *= rate;
        return temperature;
    }

    @Override
    public int nextIterations() {
        iterations = (int) (iterations / rate);
        return iterations;
    }

}
