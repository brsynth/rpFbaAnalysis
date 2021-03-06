import os
import subprocess
import sys
import tempfile

from main_test import Main_test


class Test_software(Main_test):
    @staticmethod
    def launch(args):
        if isinstance(args, str):
            args = args.split()
        ret = subprocess.run(args, capture_output=True, encoding="utf8")
        return ret

    def test_software_butanol(self):
        # Be careful: can not test gene annotation into
        # worflows running simultaneously
        with tempfile.NamedTemporaryFile(delete=False) as fd:
            args = ["python", "-m" "rpfa"]
            args += ["--input-model-file", self.model_ecoli]
            args += ["--input-pathway-file", self.pathway_butanol]
            args += ["--biomass-rxn-id", "BIOMASS_Ec_iAF1260_core_59p81M"]
            args += ["--target-rxn-id", "EX_1btol_e"]
            args += ["--substrate-rxn-id", "EX_glc__D_e"]
            args += ["--output-file", fd.name]
            args += ["--strategy", "ko"]
            args += ["--max-knockouts", "3"]
            args += ["--input-medium-file", self.medium_butanol]
            args += ["--thread", "1"]

            ret = Test_software.launch(args)
            if ret.returncode > 0:
                print(ret.stderr)
                print(ret.stdout)
                sys.exit(1)
            lines = []
            with open(fd.name) as fid:
                lines = fid.read().splitlines()
            self.assertGreater(len(lines), 1)
        os.remove(fd.name)
