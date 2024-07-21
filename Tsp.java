import java.util.ArrayList;

public class Tsp extends SimulatedAnnealing<ArrayList<Integer>> {
    ArrayList<double[]> positions = new ArrayList<>();

    public Tsp(ArrayList<double[]> positions) {
        this.positions = positions;
    }

    @Override
    ArrayList<Integer> neighbour(ArrayList<Integer> state) {
        ArrayList<Integer> newState = new ArrayList<>();
        for (int i = 0; i < state.size(); i++) {
            newState.add(state.get(i));
        }
        int k = (int) (Math.random() * state.size());
        int j = (int) (Math.random() * state.size());
        int startIndex = Math.min(j, k);
        int endIndex = Math.max(j, k);
        // System.out.println("Range : [" + startIndex + ";" + endIndex + "]");
        for (int i = startIndex; i <= endIndex; i++) {
            newState.set(endIndex + startIndex - i, state.get(i));
        }
        // System.out.println("Cost: " + cost(state));
        return newState;
    }

    double manhattenDistance(double[] x, double[] y) {
        double d = 0;
        for (int i = 0; i < x.length; i++) {
            d += Math.abs(x[i] - y[i]);
        }
        return d;
    }

    @Override
    double cost(ArrayList<Integer> state) {
        double c = 0;
        for (int i = 1; i < state.size(); i++) {
            c += manhattenDistance(positions.get(state.get(i - 1)), positions.get(state.get(i)));
        }
        return c;
    }

    @Override
    double acceptance(ArrayList<Integer> currentState, ArrayList<Integer> newState, double temperature) {
        // System.out.println("Acceptance: " + Math.min(1, Math.exp((cost(currentState)
        // - cost(newState)) / temperature)));
        return Math.min(1, Math.exp((cost(currentState) - cost(newState)) / temperature));
    }

}