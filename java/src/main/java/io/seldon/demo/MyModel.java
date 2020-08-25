package io.seldon.demo;

import com.google.protobuf.InvalidProtocolBufferException;
import io.seldon.protos.PredictionProtos.DefaultData;
import io.seldon.protos.PredictionProtos.SeldonMessage;
import io.seldon.protos.PredictionProtos.Tensor;
import io.seldon.wrapper.api.SeldonPredictionService;
import io.seldon.wrapper.pb.ProtoBufUtils;
import java.util.List;

public class MyModel implements SeldonPredictionService {

  public String predictREST(String payload) throws InvalidProtocolBufferException {
    // System.out.printf("[JAVA] Decoding raw payload from JSON\n");
    SeldonMessage.Builder builder = SeldonMessage.newBuilder();
    ProtoBufUtils.updateMessageBuilderFromJson(builder, payload);
    SeldonMessage input = builder.build();

    SeldonMessage prediction = this.predict(input);

    String rawPrediction = ProtoBufUtils.toJson(prediction, true);

    return rawPrediction;
  }

  public byte[] predictGRPC(byte[] payload) throws InvalidProtocolBufferException {
    SeldonMessage input = SeldonMessage.parseFrom(payload);

    SeldonMessage prediction = this.predict(input);
    byte[] rawPrediction = prediction.toByteArray();
    // System.out.printf("[JAVA] Raw prediction was %d elements long\n", rawPrediction.length);

    return rawPrediction;
  }

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
