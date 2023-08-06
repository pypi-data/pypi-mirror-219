from datetime import datetime
from wallaroo.assay_config import *
import json
import pytest


def test_ensure_tz():
    now = datetime.now()
    nowutz = ensure_tz(now)
    assert now != nowutz

    now = datetime.now(tz=timezone.utc)
    nowutz = ensure_tz(now)
    assert now == nowutz


def test_calc_bins():
    assert calc_bins(100_000, "auto") == "auto"
    assert calc_bins(100_000, None) == 50
    assert calc_bins(650, None) == 25
    assert calc_bins(660, None) == 25


def test_unwrap():
    v = unwrap(3)
    assert v == 3

    with pytest.raises(Exception):
        v = unwrap(None)


def test_fixed_baseline():
    pipeline_name = "mypipeline"
    model_name = "mymodel"
    bl = FixedBaseline(pipeline_name, model_name, datetime.utcnow(), datetime.now())
    json_dict = json.loads(bl.to_json())
    fixed = json_dict["Fixed"]
    assert fixed["pipeline"] == pipeline_name
    assert fixed["model"] == model_name


def test_fixed_baseline_builder():
    pipeline_name = "mypipeline"
    model_name = "mymodel"
    fbb = FixedBaselineBuilder(pipeline_name)
    print(fbb.to_json())
    jd = json.loads(fbb.to_json())
    assert jd["pipeline_name"] == pipeline_name
    assert jd["model_name"] is None
    assert jd["start"] is None
    assert jd["end"] is None

    with pytest.raises(Exception):
        jd.build()

    fbb.add_model_name(model_name)
    fbb.add_start(datetime.now())
    fbb.add_end(datetime.now())

    fb = fbb.build()
    assert fb is not None
    json_dict = json.loads(fb.to_json())
    assert json_dict["Fixed"]["model"] == model_name
    assert json_dict["Fixed"]["start_at"]


def test_summarizer_config():
    ts = SummarizerConfig()
    assert ts is not None


def test_uc_summarizer_config():
    num_bins = 10
    ucs = UnivariateContinousSummarizerConfig(
        BinMode.QUANTILE,
        Aggregation.DENSITY,
        Metric.SUMDIFF,
        num_bins,
        None,
        None,
        None,
        True,
    )
    assert ucs is not None
    ucs_dict = json.loads(ucs.to_json())
    assert ucs_dict["num_bins"] == num_bins


def test_uc_sum_builder():
    ucsb = UnivariateContinousSummarizerBuilder()
    assert ucsb is not None

    ucsb.add_aggregation(Aggregation.EDGES)
    ucsb.add_metric(Metric.MAXDIFF)

    sum_config = ucsb.build()
    sum = json.loads(sum_config.to_json())
    assert sum["num_bins"] == 5
    assert sum["type"] == "UnivariateContinuous"
    assert sum["aggregation"] == "Edges"
    assert sum["metric"] == "MaxDiff"


def test_window_config():
    wc = WindowConfig("pipeline_name", "model_name", "3 hour")
    wd = json.loads(wc.to_json())
    assert wd["model"] == "model_name"


def test_window_builder():
    pipeline_name = "mypipeline"
    model_name = "mymodel"
    wb = WindowBuilder(pipeline_name)
    wb.add_model_name(model_name)
    wb.add_width(hours=3)
    assert wb is not None
    window_dict = json.loads(wb.build().to_json())
    assert window_dict["model"] == model_name
    assert window_dict["width"] == "3 hours"


def test_config_encoder():
    d = datetime.now()
    o = {"date": d}
    with pytest.raises(Exception):
        s = json.dumps(o)

    s = json.dumps(o, default=ConfigEncoder)
    assert s is not None


def test_assay_config():
    bl = FixedBaseline("pipeline_name", "model_name", datetime.utcnow(), datetime.now())
    wc = WindowConfig("pipeline_name", "model_name", "3 hour")
    sc = UnivariateContinousSummarizerConfig(
        BinMode.QUANTILE,
        Aggregation.DENSITY,
        Metric.SUMDIFF,
        10,
        None,
        None,
        None,
        True,
    )

    ac = AssayConfig(
        None,
        "test",
        0,
        "test",
        True,
        "test",
        "inputs 0 0",
        bl,
        wc,
        sc,
        None,
        0.5,
        datetime.now(),
        None,
    )
    ad = json.loads(ac.to_json())
    print(ac.to_json())
    assert ad["name"] == "test"


def test_assay_builder():
    ab = AssayBuilder(
        None,
        "n",
        0,
        "test",
        "test",
        datetime.now(),
        datetime.now(),
        iopath="inputs 0 0",
    )
    assert ab.name == "n"
    ab.add_name("ab")

    with pytest.raises(Exception):
        ab.add_iopath("foo")

    ab.add_iopath(" inputs 0 0 ")

    ad = json.loads(ab.build().to_json())
    assert ad["name"] == "ab"
    assert ad["baseline"]["Fixed"]["pipeline"] == "test"
    assert ad["iopath"] == "inputs 0 0"


def test_assay_builder_window_width():
    assay_builder = AssayBuilder(
        None,
        "n",
        0,
        "test",
        "test",
        datetime.now(),
        datetime.now(),
        iopath="inputs 0 0",
    )
    assay_builder.window_builder().add_width(hours=12)

    acd = json.loads(assay_builder.build().to_json())
    assert acd["window"]["width"] == "12 hours"
    assert acd["window"]["start"] is None
    assert acd["window"]["interval"] is None

    assay_builder.window_builder().add_interval(hours=4)
    assay_builder.window_builder().add_start(datetime.now())
    acd = json.loads(assay_builder.build().to_json())
    assert acd["window"]["width"] == "12 hours"
    assert acd["window"]["interval"] == "4 hours"
    assert acd["window"]["start"] is not None

    # Invalid interval type
    with pytest.raises(Exception):
        assay_builder.window_builder().add_interval(fortnights=2)

    # Multiple intervals invalid
    with pytest.raises(Exception):
        assay_builder.window_builder().add_interval(weeks=1, hours=4)


def test_assay_builder_bin_settings():
    weights = [1.0] * 7

    ab = AssayBuilder(
        None,
        "n",
        0,
        "test",
        "test",
        datetime.now(),
        datetime.now(),
        iopath="inputs 0 0",
    )
    with pytest.raises(Exception):
        ab.summarizer_builder.add_bin_weights([1])

    ab.summarizer_builder.add_bin_weights(weights)

    ad = json.loads(ab.build().to_json())
    print(ad["summarizer"])
    print(ad["summarizer"]["bin_weights"])
    assert ad["summarizer"]["bin_weights"] == weights

    with pytest.raises(Exception):
        ab.summarizer_builder.add_num_bins(7)

    ab.summarizer_builder.add_bin_weights(None)
    ab.summarizer_builder.add_num_bins(7)

    ad = json.loads(ab.build().to_json())
    print(ad["summarizer"])
    print(ad["summarizer"]["bin_weights"])
    assert ad["summarizer"]["bin_weights"] is None
    assert ad["summarizer"]["num_bins"] == 7


def test_assay_builder_add_edges():
    edges = [1.0] * 6

    ab = AssayBuilder(
        None,
        "n",
        0,
        "test",
        "test",
        datetime.now(),
        datetime.now(),
        iopath="inputs 0 0",
    )
    # too few edges
    with pytest.raises(Exception):
        ab.summarizer_builder.add_bin_edges([1])

    # edges == to number of bins
    ab.summarizer_builder.add_bin_edges(edges[1:])
    # edges specifying left outlier
    ab.summarizer_builder.add_bin_edges(edges)

    # too many edges
    with pytest.raises(Exception):
        ab.summarizer_builder.add_bin_edges([1.0] * 8)

    # check that that we can't build with the wrong bin mode
    with pytest.raises(Exception):
        ad = json.loads(ab.build().to_json())

    # check that the edges get into the json and back
    ab.summarizer_builder.add_bin_mode(BinMode.PROVIDED, edges)
    ad = json.loads(ab.build().to_json())

    print(ad["summarizer"])
    print(ad["summarizer"]["provided_edges"])
    assert ad["summarizer"]["provided_edges"] == edges

    # try to change num bins
    moar_bins = 10
    with pytest.raises(Exception):
        ab.summarizer_builder.add_num_bins(moar_bins)

    # clear out the edges and add more bins
    ab.summarizer_builder.add_bin_mode(BinMode.EQUAL)
    ab.summarizer_builder.add_num_bins(moar_bins)

    ad = json.loads(ab.build().to_json())
    print(ad["summarizer"])
    print(ad["summarizer"]["provided_edges"])
    assert ad["summarizer"]["provided_edges"] is None
    assert ad["summarizer"]["num_bins"] == moar_bins

    ab.summarizer_builder.add_bin_mode(BinMode.PROVIDED, [1.0] * moar_bins)
    ad = json.loads(ab.build().to_json())
    assert len(ad["summarizer"]["provided_edges"]) == moar_bins
