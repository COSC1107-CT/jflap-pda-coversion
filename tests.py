import pda_converter


def test_should_convert_pda():
    pda_converter.convert_pda("./samples/PDA-example.jff", "./test-out.jff")

