#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from human import get_intent


def test_web_open_browser():
    assert get_intent('open firefox').get('topScoringIntent').get('intent') == 'web.open_browser'
    assert get_intent('close browser').get('topScoringIntent').get('intent') == 'web.close_browser'
    assert get_intent('title should be "Facebook"').get('topScoringIntent').get('intent') == 'web.assert_title'
