
killBlockKeys=["DO-DELETE-WHEN-IMPLEMENTING exception"]

# Raw data section.
# To extend for application, copy one of these and extend the copy.
#
cxxKillKeys=[
"XInsert-Code-Here"
]

javaKillKeys=[
"XInsert-Code-Here"
]

f90KillKeys=[
"XInsert-Code-Here"
]

f77KillKeys=[
"XInsert-Code-Here"
]

pythonKillKeys=[
"XInsert-Code-Here"
]

cKillKeys=[
"XInsert-Code-Here"
]


# typically we would want to use killByLang if possible
killByLang = dict()
killByLang['f77'] = f77KillKeys
killByLang['f77_31'] = killByLang['f77']
killByLang['f90'] = f90KillKeys
killByLang['f03'] = killByLang['f90']
killByLang['python'] = pythonKillKeys
killByLang['c'] = cKillKeys
killByLang['cxx'] = cxxKillKeys
killByLang['java'] = javaKillKeys


