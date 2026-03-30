"""登录模块测试."""

from qqmusic_api import Client
from qqmusic_api.models.login import (
    PhoneAuthCodeResult,
    PhoneLoginEvents,
    QRCodeLoginEvents,
    QRLoginResult,
    QRLoginType,
)
from qqmusic_api.modules.login import LoginApi
from qqmusic_api.modules.login_utils import PhoneLoginSession, QRCodeLoginSession


async def test_get_qrcode_qq(client: Client) -> None:
    """测试获取 QQ 登录二维码."""
    result = await client.login.get_qrcode(login_type=QRLoginType.QQ)
    assert result is not None
    assert result.data is not None
    assert result.qr_type == QRLoginType.QQ


async def test_get_qrcode_wx(client: Client) -> None:
    """测试获取微信登录二维码."""
    result = await client.login.get_qrcode(login_type=QRLoginType.WX)
    assert result is not None
    assert result.data is not None
    assert result.qr_type == QRLoginType.WX


async def test_get_qrcode_mobile(client: Client) -> None:
    """测试获取手机客户端登录二维码."""
    result = await client.login.get_qrcode(login_type=QRLoginType.MOBILE)
    assert result is not None
    assert result.data is not None
    assert result.qr_type == QRLoginType.MOBILE


def test_qrcode_login_result_done_property() -> None:
    """测试二维码登录结果对象语义."""
    done_result = QRLoginResult(event=QRCodeLoginEvents.DONE)
    timeout_result = QRLoginResult(event=QRCodeLoginEvents.TIMEOUT)

    assert done_result.credential is None
    assert done_result.done is True
    assert timeout_result.done is False


def test_phone_authcode_result_semantics() -> None:
    """测试手机验证码发送结果对象语义."""
    send_result = PhoneAuthCodeResult(event=PhoneLoginEvents.SEND)
    captcha_result = PhoneAuthCodeResult(event=PhoneLoginEvents.CAPTCHA, info="https://captcha.example")

    assert send_result.info is None
    assert send_result.event == PhoneLoginEvents.SEND
    assert captcha_result.info == "https://captcha.example"


def test_phone_login_session_contract() -> None:
    """测试手机验证码 session 保存必要状态."""
    login_api = object.__new__(LoginApi)
    session = PhoneLoginSession(login_api, 13000000000)
    assert session.api is login_api
    assert session.phone == 13000000000
    assert session.country_code == 86
    assert session.last_result is None


def test_qrcode_login_session_contract() -> None:
    """测试二维码登录 session 保存必要状态."""
    login_api = object.__new__(LoginApi)
    session = QRCodeLoginSession(
        login_api,
        QRLoginType.QQ,
        interval=2.0,
        timeout_seconds=90.0,
        emit_repeat=True,
    )
    assert session.api is login_api
    assert session.login_type == QRLoginType.QQ
    assert session.qrcode is None
    assert session.interval == 2.0
    assert session.timeout_seconds == 90.0
    assert session.emit_repeat is True
