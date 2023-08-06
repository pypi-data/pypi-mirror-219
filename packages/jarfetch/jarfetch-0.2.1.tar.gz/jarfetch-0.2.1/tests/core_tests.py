from typing import get_args

from jarfetch.client import ServerJars
from jarfetch.data_models import JarType, JarCat, allowed, JarDetails, FullJarDetails
from jarfetch.functional import match_category


class ClientObjectTests:
    def __init__(self):
        self.standard = ServerJars()
        self.danger = ServerJars(force_unsafe_ignore_hash=True)

        # standard types
        self.ss_types = []      # single types
        self.sn_types = {}      # nested types
        self.sf_types = []      # flat types

        # standard categories (sc) dicts, keyed to category
        self.sc_raw_details = {}    # raw details
        self.sc_fraw_details = {}   # full raw details
        self.sc_dc_details = {}     # dataclass details
        self.sc_fdc_details = {}    # full dataclass details
        self.sc_versions = {}       # all versions for each cat (=key)
        self.sc_sf_details = {}     # specific (oldest) version full details
        self.sc_s5r_details = {}    # limited (5) details

        # danger types
        self.ds_types = []
        self.dn_types = []
        self.df_types = []

    def base_client(self):
        assert isinstance(self.standard, ServerJars)

    def keyword_client(self):
        assert isinstance(self.danger, ServerJars)

    def positional_client(self):
        sj_invalid, e = None, None
        try:
            sj_invalid = ServerJars(True)
        except TypeError as e:
            pass
        assert isinstance(e, TypeError) and not sj_invalid

    def nested_types(self):
        self.sn_types = self.standard.jar_types()
        assert isinstance(self.sn_types, dict)

    def flat_types(self):
        self.sf_types = self.standard.jar_types(flatten=True)
        assert isinstance(self.sf_types, list)

    def literal_type_alignment(self):
        expected_types = get_args(JarType)
        fetched = self.sn_types.keys()
        assert len(fetched) == len(expected_types)
        for x in fetched:
            assert x in expected_types

    def literal_cat_alignment(self):
        expected_cats = get_args(JarCat)
        fetched = self.sf_types
        assert len(expected_cats) == len(fetched)
        for x in fetched:
            assert x in expected_cats

    def match_checks(self):
        for k in allowed:
            fetched_flat = self.standard.jar_types(single_type=k, flatten=True)
            assert isinstance(fetched_flat, list)
            fetched_dict = self.standard.jar_types(single_type=k)
            assert isinstance(fetched_dict, dict)
            assert fetched_flat == fetched_dict[k] == allowed[k]
            for v in allowed[k]:
                assert match_category(v) == k

    def latest_details_parser(self):
        for c in self.sf_types:
            cur = self.sc_raw_details[c] = self.standard.jar_details(c, raw=True)
            assert isinstance(cur, dict)
            cur = self.sc_fraw_details[c] = self.standard.jar_details(c, raw=True, backfill=True)
            assert isinstance(cur, dict)
            cur = self.sc_dc_details[c] = self.standard.jar_details(c)
            assert isinstance(cur, JarDetails)
            cur = self.sc_fdc_details[c] = self.standard.jar_details(c, backfill=True)
            assert isinstance(cur, FullJarDetails)
            assert cur.latest

    def versions_nolimit_details(self):
        for c in self.sf_types:
            cur = self.sc_versions[c] = self.standard.jar_versions(c)

            # versions available
            assert bool(cur)

            # return is a list of strings
            assert isinstance(cur, list)
            assert isinstance(cur[0], str)


    def limited_cat_details_parse(self):
        for i, c in enumerate(self.sf_types):
            # test default works
            self.standard.multi_jar_details(c, limit=5) if i % 2 else self.standard.multi_jar_details(c)

    def specific_oldest_details(self):
        for c in self.sf_types:
            # select oldest version
            v = self.sc_versions[c][-1]
            # request backfilled specific version
            cur = self.sc_sf_details[c] = self.standard.jar_details(c, version=v, backfill=True)
            # ensure correct parsing and ability to backfill for each category
            assert isinstance(cur, FullJarDetails)

            # ensure correct latest assignment
            # latest should not be true, assuming there isn't only one available version (oldest was selected)
            assert cur.latest is not (len(self.sc_versions[c]) > 1)

            # ensure version alignment between requested and received
            assert cur.version == v

            # version should be a part of the file string
            assert v in cur.file

    def expected_bytes_latest(self):
        # stream provides specified bytes
        pass

    def expected_bytes_specific(self):
        pass

    def bad_hash_fail(self):
        # stream failure for standard
        pass

    def bad_hash_succeed(self):
        # stream success for danger
        pass

    def good_hash_write(self):
        # standard download success
        pass

    def good_hash_write_alt(self):
        # standard write to specified location
        pass

    def danger_good_write(self):
        pass

    def bad_hash_no_write(self):
        pass

    def x(self):
        pass

