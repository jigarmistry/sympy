from sympy.combinatorics.named_groups import SymmetricGroup, DihedralGroup,\
CyclicGroup, AlternatingGroup
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.util import _check_cycles_alt_sym, _strip,\
_distribute_gens_by_base, _strong_gens_from_distr,\
_orbits_transversals_from_bsgs, _handle_precomputed_bsgs, _base_ordering,\
_verify_bsgs

def test_check_cycles_alt_sym():
    perm1 = Permutation([[0, 1, 2, 3, 4, 5, 6], [7], [8], [9]])
    perm2 = Permutation([[0, 1, 2, 3, 4, 5], [6, 7, 8, 9]])
    perm3 = Permutation([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    assert _check_cycles_alt_sym(perm1) == True
    assert _check_cycles_alt_sym(perm2) == False
    assert _check_cycles_alt_sym(perm2) == False

def test_strip():
    D = DihedralGroup(5)
    D.schreier_sims()
    member = Permutation([4, 0, 1, 2, 3])
    not_member1 = Permutation([0, 1, 4, 3, 2])
    not_member2 = Permutation([3, 1, 4, 2, 0])
    identity = Permutation([0, 1, 2, 3, 4])
    res1 = _strip(member, D.base, D.basic_orbits, D.basic_transversals)
    res2 = _strip(not_member1, D.base, D.basic_orbits, D.basic_transversals)
    res3 = _strip(not_member2, D.base, D.basic_orbits, D.basic_transversals)
    assert res1[0] == identity
    assert res1[1] == len(D.base) + 1
    assert res2[0] == not_member1
    assert res2[1] == len(D.base) + 1
    assert res3[0] != identity
    assert res3[1] == 2

def test_distribute_gens_by_base():
    base = [0, 1, 2]
    gens = [Permutation([0, 1, 2, 3]), Permutation([0, 1, 3, 2]),\
           Permutation([0, 2, 3, 1]), Permutation([3, 2, 1, 0])]
    assert _distribute_gens_by_base(base, gens) == [gens,\
                                                   [Permutation([0, 1, 2, 3]),\
                                                   Permutation([0, 1, 3, 2]),\
                                                   Permutation([0, 2, 3, 1])],\
                                                   [Permutation([0, 1, 2, 3]),\
                                                   Permutation([0, 1, 3, 2])]]

def test_strong_gens_from_distr():
    distr_gens = [[Permutation([0, 2, 1]), Permutation([1, 2, 0]),\
                  Permutation([1, 0, 2])], [Permutation([0, 2, 1])]]
    assert _strong_gens_from_distr(distr_gens) ==\
                                                     [Permutation([0, 2, 1]),\
                                                     Permutation([1, 2, 0]),\
                                                     Permutation([1, 0, 2])]

def test_orbits_transversals_from_bsgs():
    S = SymmetricGroup(4)
    S.schreier_sims()
    base = S.base
    strong_gens = S.strong_gens
    distr_gens = _distribute_gens_by_base(base, strong_gens)
    result = _orbits_transversals_from_bsgs(base, distr_gens)
    orbits = result[0]
    transversals = result[1]
    base_len = len(base)
    for i in range(base_len):
        for el in orbits[i]:
            assert transversals[i][el](base[i]) == el
            for j in range(i):
                assert transversals[i][el](base[j]) == base[j]
    order = 1
    for i in range(base_len):
        order *= len(orbits[i])
    assert S.order() == order

def test_handle_precomputed_bsgs():
    A = AlternatingGroup(5)
    A.schreier_sims()
    base = A.base
    strong_gens = A.strong_gens
    result = _handle_precomputed_bsgs(base, strong_gens)
    distr_gens = _distribute_gens_by_base(base, strong_gens)
    assert distr_gens == result[2]
    transversals = result[0]
    orbits = result[1]
    base_len = len(base)
    for i in range(base_len):
        for el in orbits[i]:
            assert transversals[i][el](base[i]) == el
            for j in range(i):
                assert transversals[i][el](base[j]) == base[j]
    order = 1
    for i in range(base_len):
        order *= len(orbits[i])
    assert A.order() == order

def test_base_ordering():
    base = [2, 4, 5]
    degree = 7
    assert _base_ordering(base, degree) == [3, 4, 0, 5, 1, 2, 6]

def test_verify_bsgs():
    S = SymmetricGroup(5)
    S.schreier_sims()
    base = S.base
    strong_gens = S.strong_gens
    gens = S.generators
    assert _verify_bsgs(S, base, strong_gens) == True
    assert _verify_bsgs(S, base[:-1], strong_gens) == False
    assert _verify_bsgs(S, base, S.generators) == False