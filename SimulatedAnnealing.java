public abstract class SimulatedAnnealing<T> {
    public abstract class AnnealingSchedule {
        abstract boolean hasNext();

        abstract double nextTemperature();

        abstract int nextIterations();
    }

    abstract T neighbour(T state);

    abstract double cost(T state);

    abstract double acceptance(T currentState, T newState, double temperature);

    public T run(T initialState, AnnealingSchedule schedule) {
        T currentState = initialState;
        while (schedule.hasNext()) {
            double temperature = schedule.nextTemperature();
            int iterations = schedule.nextIterations();
            for (int i = 0; i < iterations; i++) {
                T newState = this.neighbour(currentState);
                double acceptance = acceptance(currentState, newState, temperature);
                if (acceptance >= Math.random()) {
                    currentState = newState;
                }
            }
        }
        return currentState;
    }
}