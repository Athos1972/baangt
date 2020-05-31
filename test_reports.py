from baangt.reports import Dashboard, Summary

name = 'example_googleImages.xlsx'
#name = 'paypal_secondform2.xlsx'
stage = 'Debug'
#stage = 'Test'

#d = Dashboard(name=name, stage=stage)
#d = Dashboard(name=name)
#d = Dashboard(stage=stage)
#d = Dashboard()
#d.show()

#uuid = 'bdf3e0e2-e0e9-4289-810b-e3c773ebb7ce'
#uuid = 'fd5d3557-1b7f-4995-bc10-73155e5a686e'
uuid = '56ad6a1f-0641-4b2d-82f2-05e11a84d46c'

r = Summary(uuid)
r.show()