//
//  ViewController.swift
//  Login_Navigation
//
//  Created by 최원일 on 5/27/25.
//

import UIKit

class MyPageBeforeViewController: UIViewController {

    /// 기본적으로 생기는 네비게이션 왼쪽 아이템 숨기기
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        // 네비게이션 뒤로가기 버튼 숨기기
        self.navigationItem.hidesBackButton = true
        // 네비게이션 바 숨기기
        self.navigationController?.setNavigationBarHidden(true, animated: false)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

    @IBAction func BackButton(_ sender: UIButton) {
        // 현재 뷰에서, 이전 뷰로 돌아가고 싶을 때
        if let navigationController = self.navigationController {
            navigationController.popViewController(animated: true)
        } else {
            self.dismiss(animated: true, completion: nil)
        }
    }
    
}


