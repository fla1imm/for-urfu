try:
        source = (
            variant[
                "test_data"
            ]()
        )

        result = (
            prepare_benchmark(
                source
            )
        )

        checks = (
            variant["check"](
                result,
                source,
            )
        )


