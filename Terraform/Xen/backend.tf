terraform {
  backend "http" {
    address        = "http://192.168.1.9:9961/v1/state/xenomorph"
    lock_address   = "http://192.168.1.9:9961/v1/lock/xenomorph"
    unlock_address = "http://192.168.1.9:9961/v1/unlock/xenomorph"
    lock_method    = "POST"
    unlock_method  = "POST"
  }
}
