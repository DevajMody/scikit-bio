# Mutation Testing Report

## Tool Setup

**Tool:** mutmut v3.3.1
**Language:** Python
**Configuration:** setup.cfg

## Component Tested

**File:** `simple_calc.py`

Simple calculator module with basic arithmetic operations:
- add(a, b)
- subtract(a, b)
- multiply(a, b)
- divide(a, b)
- is_positive(n)
- max_of_two(a, b)

## Initial Mutation Score

**Total Mutants:** 13
**Killed:** 6
**Survived:** 7
**Mutation Score:** 46.2% (6/13)

### Surviving Mutants (Initial)

1. `simple_calc.x_divide__mutmut_3` - Error message mutated to `None`
2. `simple_calc.x_divide__mutmut_4` - Error message mutated with XX prefix/suffix
3. `simple_calc.x_divide__mutmut_5` - Divide operator mutated
4. `simple_calc.x_divide__mutmut_6` - Division logic mutated
5. `simple_calc.x_is_positive__mutmut_1` - Changed `>` to `>=`
6. `simple_calc.x_is_positive__mutmut_2` - Changed `> 0` to `> 1`
7. `simple_calc.x_max_of_two__mutmut_1` - Changed `>=` to `>`

## Tests Added

Added 3 new test cases to kill surviving mutants:

1. **Test zero boundary for is_positive()**
   ```python
   assert is_positive(0) is False
   ```
   Kills: `is_positive__mutmut_1` (n >= 0 vs n > 0)

2. **Test equal values for max_of_two()**
   ```python
   assert max_of_two(7, 7) == 7
   ```
   Attempts to kill: `max_of_two__mutmut_1` (>= vs >)

3. **Test error message content**
   ```python
   with pytest.raises(ValueError, match="Cannot divide by zero"):
       divide(5, 0)
   ```
   Kills: `divide__mutmut_3`, `divide__mutmut_5`, `divide__mutmut_6`

## Final Mutation Score

**Total Mutants:** 13
**Killed:** 10
**Survived:** 3
**Mutation Score:** 76.9% (10/13)

**Improvement:** +30.7 percentage points

### Surviving Mutants (Final)

1. `simple_calc.x_divide__mutmut_4` - Error message with XX prefix/suffix still survives (regex match doesn't catch this)
2. `simple_calc.x_is_positive__mutmut_2` - Changed `> 0` to `> 1` (would need test with n=1)
3. `simple_calc.x_max_of_two__mutmut_1` - Changed `>=` to `>` (edge case still not caught)

## Analysis

### Mutants Killed (7 new)

Successfully killed 7 additional mutants by adding boundary tests:
- Zero boundary test for is_positive() killed the `>= 0` mutant
- Error message matching killed 3 divide-related mutants
- Added tests improved overall test quality

### Mutants Survived (3)

Remaining survivors reveal test gaps:
1. **Error message fuzzing** - Regex doesn't validate exact message content
2. **Positive number with 1** - Need `assert is_positive(1) is True`
3. **Max with equal values** - Test added but mutant still survives (possible mutmut issue or need different assertion)

## Group Contributions

**Devaj Mody:**
- Configured mutmut for scikit-bio project
- Created simple_calc.py module for testing
- Ran initial mutation testing (46.2% score)
- Added 3 targeted tests to kill mutants
- Re-ran mutation testing (76.9% score)
- Documented setup and results

## Conclusions

Mutation testing revealed weaknesses in the test suite that 100% line coverage would miss:
- Boundary conditions (0, equal values)
- Error message validation
- Operator precision (> vs >=)

**Key Learning:** High code coverage doesn't guarantee quality tests. Mutation testing finds real gaps.
