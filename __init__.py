Model 1
def compare_generic_social(self, period, cG, cN, eG, eN, friends, utility_handler):
    util_green, util_normal = self.evaluate_green_normal_social(utility_handler, cG,
                                                        cN, eG, eN, friends, period)

    # compare utilities
    green_is_better = util_green > util_normal # evaluates boolean

    if green_is_better:
        self.assign_green_social(period, utility_handler, eG, cG)
        self.assign_budget_and_utilities_disparity(period, util_green, util_normal)
        return util_green

    else:
        self.assign_normal_social(period, utility_handler, eN, cN)
        self.assign_budget_and_utilities_disparity(period, util_green, util_normal)
        return util_normal
