import pytest
from unicorndrop.packages.domain_models.transfer import Transfer, TransferStatus, content_sha256
def test_transfer_lifecycle_and_hash():
    t = Transfer("t1", "idem1", content_sha256(b"payload"))
    t.move(TransferStatus.ACCEPTING, "operator")
    t.move(TransferStatus.RECEIVED, "gateway")
    assert t.status == TransferStatus.RECEIVED
    assert len(t.audit) == 2
def test_invalid_transition_rejected():
    t = Transfer("t1", "idem1", content_sha256(b"x"))
    with pytest.raises(ValueError): t.move(TransferStatus.DELIVERED, "system")
