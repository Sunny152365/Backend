//
//  ViewController.swift
//  Login_Navigation
//
//  Created by 최원일 on 5/27/25.
//

import UIKit

class MyPageAfterLoginViewController: UIViewController {

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

    @IBAction func initialButton(_ sender: UIButton) {
        // 초기 화면(1번째 화면) 으로
        // self.navigationController?.popToRootViewController(animated: true)
        // 예: 루트 뷰컨트롤러를 로그인 화면으로 변경
        if let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
           let sceneDelegate = windowScene.delegate as? UIWindowSceneDelegate,
           let window = sceneDelegate.window ?? (sceneDelegate as? SceneDelegate)?.window {
            
            let storyboard = UIStoryboard(name: "Main", bundle: nil)
            let loginVC = storyboard.instantiateViewController(withIdentifier: "MainPageViewController")
            window.rootViewController = loginVC
            window.makeKeyAndVisible()
        }
    }
    
}

