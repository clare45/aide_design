import unittest
from aide_design.units import unit_registry as u
import numpy as np
import aide_design.pipeline_utility as pipeline



class PipelineUtilityTest(unittest.TestCase):
    def test_pipeline_flow(self):
        flow = pipeline.flow_pipeline(np.array([3,4,5])*u.inch, np.array([3,4,5])*u.m, np.array([3,4,5]), 5 *u.m)
        self.assertAlmostEqual(flow.magnitude, 0.018149097841279497 * u.m**3 / u.s)


if __name__ == '__main__':
    unittest.main()
