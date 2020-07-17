package io.seldon.demo;

import io.seldon.protos.PredictionProtos.DefaultData;
import io.seldon.protos.PredictionProtos.SeldonMessage;
import io.seldon.protos.PredictionProtos.Tensor;
import io.seldon.wrapper.api.SeldonPredictionService;
import java.util.List;

public class MyModel implements SeldonPredictionService {

  @Override
  public SeldonMessage predict(SeldonMessage payload) {
    List<Double> values = payload.getData().getTensor().getValuesList();
    // System.out.printf("[JAVA] Input was %d elements long\n", values.size());

    Double total = 0.0;
    for (Double val : values) {
      total += val;
    }
    // System.out.printf("[JAVA] Total was %.2f\n", total);

    return SeldonMessage.newBuilder()
        .setData(
            DefaultData.newBuilder().setTensor(Tensor.newBuilder().addValues(total).addShape(1)))
        .build();
  }
}
