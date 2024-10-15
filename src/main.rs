use rsolace::solclient::{SessionProps, SolClient};
use rsolace::types::{SolClientLogLevel, SolClientSubscribeFlags};
use tracing_subscriber;

fn main() {
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::DEBUG)
        .init();
    let mut solclient = SolClient::new(SolClientLogLevel::Notice).unwrap();
    let props = SessionProps::default()
        .host("128.110.5.101:55555")
        .vpn("sp-intra")
        .username("ap01")
        .password("password")
        .client_name("sb2solace_sub_rs")
        .compression_level(0);
    let r = solclient.connect(props);
    tracing::info!("connected: {}", r);
    let sub_r = solclient.subscribe_ext("R/F/S/>", SolClientSubscribeFlags::WaitForConfirm);
    tracing::info!("subscribed: {:?}", sub_r);
    let receiver = solclient.get_msg_receiver();
    loop {
        match receiver.recv() {
            Ok(msg) => {
                msg.dump(true);
            }
            Err(e) => {
                tracing::error!("recv msg error: {:?}", e);
                break;
            }
        }
    }
}
