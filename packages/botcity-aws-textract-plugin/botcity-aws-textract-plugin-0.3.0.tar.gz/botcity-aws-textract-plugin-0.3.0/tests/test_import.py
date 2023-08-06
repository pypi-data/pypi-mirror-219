def test_package_import():
    import botcity.plugins.aws.textract as plugin
    assert plugin.__file__ != ""
