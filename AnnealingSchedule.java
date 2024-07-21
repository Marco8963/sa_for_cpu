public interface AnnealingSchedule {
    abstract boolean hasNext();

    abstract double nextTemperature();

    abstract int nextIterations();
}
