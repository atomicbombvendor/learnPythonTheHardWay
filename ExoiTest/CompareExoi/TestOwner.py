from ExoiTest.CompareExoi.Ownership.OwnershipSummary import OwnershipSummary
from ExoiTest.CompareExoi.Ownership.OwnershipMonthlySummary import OwnershipMonthlySummary

owner = OwnershipMonthlySummary()
owner.get_content("0P000000GY|41004|45826946|2013-06-30|")
print owner.check_value("0P000000GY|41004|45826946|2013-06-30|")

print owner.content